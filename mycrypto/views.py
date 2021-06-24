import sqlite3
import requests
from flask.json import jsonify
from mycrypto import app
from mycrypto.dataaccess import DBmanager
from flask import jsonify, render_template, request, Response
from http import HTTPStatus
from config import API_KEY_COINMARKET


dbManager = DBmanager(app.config.get('DATABASE')) # instancia de la clase DBmanager

def calculaSaldoFrom(query):
    lista = dbManager.consultaMuchasSQL(query)
    saldoFrom = 0
    for i in range(len(lista)):
        saldoFrom += lista[i]['cantidad_from']
    return saldoFrom

def calculaSaldoTo(query):
    lista = dbManager.consultaMuchasSQL(query)
    saldoTo = 0
    for i in range(len(lista)):
        saldoTo += lista[i]['cantidad_to']
    return saldoTo



@app.route('/')
def listaMovimientos():
    return render_template('mycrypto.html')



@app.route('/api/v1/movimientos')  # método GET por defecto, muestra lista de movimientos
def movimientosAPI():
    query = "SELECT * FROM movimientos ORDER BY date;"
    
    try:
        lista = dbManager.consultaMuchasSQL(query)
        return jsonify({'status': 'success', 'movimientos': lista})
    except sqlite3.Error as e:
        return jsonify({'status': 'fail', 'mensaje': str(e)})



@app.route("/api/v1/movimiento/<int:id>", methods=['GET']) # muestra un movimiento
@app.route("/api/v1/movimiento", methods=['POST'])  # grabamos un nuevo movimiento
def detalleMovimiento(id=None):
    try:
        if request.method == 'GET':
            movimiento = dbManager.consultaUnaSQL("SELECT * FROM movimientos WHERE id = ?", [id])
    
            if movimiento:
                return jsonify({
                    "status": "success",
                    "movimiento": movimiento
            })
            else:
                return jsonify({"status": "fail", "mensaje": "movimiento no encontrado"}), HTTPStatus.NOT_FOUND



        if request.method == 'POST':
            dbManager.modificaTablaSQL("""
                INSERT INTO movimientos (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to)
                VALUES (:date, :time, :moneda_from, :cantidad_from, :moneda_to, :cantidad_to)""", request.json)

            return jsonify({"status": "success", "mensaje": "registro creado"}), HTTPStatus.CREATED

   
    except sqlite3.Error as e:
        print("error", e)
        return jsonify({"status": "fail", "mensaje": "Error en base de datos: {}".format(e)}), HTTPStatus.BAD_REQUEST
        


@app.route('/api/v1/par/<_from>/<_to>/<quantity>')
@app.route('/api/v1/par/<_from>/<_to>')
def par(_from, _to, quantity = 1.0):
    url = f"https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={quantity}&symbol={_from}&convert={_to}&CMC_PRO_API_KEY={API_KEY_COINMARKET}"
    res = requests.get(url)
    return Response(res)



@app.route('/api/v1/status')  # método GET por defecto, muestra el estado de nuestra inversión
def statusAPI():
    
    cryptos = ('BTC', 'ETH')
    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert=EUR&CMC_PRO_API_KEY={}'
        
    query1 = "SELECT cantidad_from FROM movimientos WHERE moneda_from='EUR';"
    query2 = "SELECT cantidad_to FROM movimientos WHERE moneda_to='EUR';"
    query3 = "SELECT cantidad_from FROM movimientos WHERE moneda_from='BTC';"
    query4 = "SELECT cantidad_to FROM movimientos WHERE moneda_to='BTC';"
    query5 = "SELECT cantidad_from FROM movimientos WHERE moneda_from='ETH';"
    query6 = "SELECT cantidad_to FROM movimientos WHERE moneda_to='ETH';"


    try:
        # Calculamos saldoFromEur, que coincide con el total de euros invertidos
        saldoFromEur = calculaSaldoFrom(query1)
        print("saldoFrom EUR: {}".format(saldoFromEur))

        # Calculamos saldoToEur
        saldoToEur = calculaSaldoTo(query2)
        print("saldoTo EUR: {}".format(saldoToEur))

        # Calculamos el saldo de euros invertidos (saldoToEur - saldoFromEur)
        saldoEurosInv = saldoToEur - saldoFromEur
        print("saldo euros invertidos: {}".format(saldoEurosInv))

        # Calculamos el valor de euros de nuestras Cryptos
            # BTC
        saldoFromBtc = calculaSaldoFrom(query3)
        print("saldoFrom BTC: {}".format(saldoFromBtc))

        saldoToBtc = calculaSaldoTo(query4)
        print("saldoTo BTC: {}".format(saldoToBtc))

        saldoBtc = saldoToBtc - saldoFromBtc
        print("saldo BTC: {}".format(saldoBtc))

        respuestaBtc = requests.get(url.format(saldoBtc, cryptos[0], API_KEY_COINMARKET)).json()
        #### GESTIÓN DE ERRORES ####
        print("respuesta Btc *********: {}". format(respuestaBtc))

        valorBtc = respuestaBtc['data']['quote']['EUR']['price']
        print("VALOR BTC *********: {}". format(valorBtc))

        if respuestaBtc['status']['error_code'] != 0:
            return jsonify({'status': 'fail', 'mensaje': respuestaBtc['status']['error_message']})

    
            # ETH
        print("**********************")
        print("**********************")
        saldoFromEth = calculaSaldoFrom(query5)
        print("saldoFrom ETH: {}".format(saldoFromEth))

        saldoToEth = calculaSaldoTo(query6)
        print("saldoTo ETH: {}".format(saldoToEth))

        saldoEth = saldoToEth - saldoFromEth
        print("saldo ETH: {}".format(saldoEth))

        respuestaEth = requests.get(url.format(saldoEth, cryptos[1], API_KEY_COINMARKET)).json()
        #### GESTIÓN DE ERRORES ####
        print("respuesta Eth *********: {}". format(respuestaEth))

        valorEth = respuestaEth['data']['quote']['EUR']['price']
        print("VALOR ETH *********: {}". format(valorEth))

        if respuestaEth['status']['error_code'] != 0:
            return jsonify({'status': 'fail', 'mensaje': respuestaEth['status']['error_message']})


            # TOTAL
        valorCryptos = valorBtc + valorEth

        # Calculamos el valor actual de la inversión (saldoFromEur + saldoEurosInv + valorCryptos)
        valorActualInv = saldoToEur + valorCryptos
        

        return jsonify({'status': 'success', 'data': {"invertido": saldoFromEur, "valor_actual": valorActualInv}})
    

    except sqlite3.Error as e:
        return jsonify({'status': 'fail', 'mensaje': str(e)})




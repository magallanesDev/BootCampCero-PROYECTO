import sqlite3
import requests
from flask.json import jsonify
from mycrypto import app
from mycrypto.dataaccess import DBmanager
from flask import jsonify, render_template, request, Response
from http import HTTPStatus
from config import API_KEY_COINMARKET

cryptos = ('BTC', 'ETH')
dbManager = DBmanager(app.config.get('DATABASE')) # instancia de la clase DBmanager


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
def statusAPI2():
    query1 = "SELECT cantidad_from FROM movimientos WHERE moneda_from='EUR';"
    query2 = "SELECT cantidad_to FROM movimientos WHERE moneda_to='EUR';"
    query3 = "SELECT cantidad_from FROM movimientos WHERE moneda_from='BTC';"
    query4 = "SELECT cantidad_to FROM movimientos WHERE moneda_to='BTC';"
    query5 = "SELECT cantidad_from FROM movimientos WHERE moneda_from='ETH';"
    query6 = "SELECT cantidad_to FROM movimientos WHERE moneda_to='ETH';"


    try:
        # Calculamos saldoFromEur, que coincide con el total de euros invertidos
        lista1 = dbManager.consultaMuchasSQL(query1)
        print(lista1)
        saldoFromEur = 0
        for i in range(len(lista1)):
            saldoFromEur += lista1[i]['cantidad_from']
        print("saldoFrom EUR: {}".format(saldoFromEur))

        # Calculamos saldoToEur
        lista2 = dbManager.consultaMuchasSQL(query2)
        print(lista2)
        saldoToEur = 0
        for i in range(len(lista2)):
            saldoToEur += lista2[i]['cantidad_to']
        print("saldoTo EUR: {}".format(saldoToEur))

        # Calculamos el saldo de euros invertidos (saldoToEur - saldoFromEur)
        saldoEurosInv = saldoToEur - saldoFromEur
        print("saldo euros invertidos: {}".format(saldoEurosInv))

        # Calculamos el valor de euros de nuestras Cryptos
            # BTC
        lista3 = dbManager.consultaMuchasSQL(query3)
        print(lista3)
        saldoFromBtc = 0
        for i in range(len(lista3)):
            saldoFromBtc += lista3[i]['cantidad_from']
        print("saldoFrom BTC: {}".format(saldoFromBtc))

        lista4 = dbManager.consultaMuchasSQL(query4)
        print(lista4)
        saldoToBtc = 0
        for i in range(len(lista4)):
            saldoToBtc += lista4[i]['cantidad_to']
        print("saldoTo BTC: {}".format(saldoToBtc))

        saldoBtc = saldoToBtc - saldoFromBtc
        print("saldo BTC: {}".format(saldoBtc))

        url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol=BTC&convert=EUR&CMC_PRO_API_KEY={}'
        
        respuestaBtc = requests.get(url.format(saldoBtc, API_KEY_COINMARKET))
        #### GESTIÓN DE ERRORES ####
        print("respuesta Btc *********: {}". format(respuestaBtc))
        respuestaBtcJson = respuestaBtc.json()
        print("respuesta Btc 2 *********: {}". format(respuestaBtcJson))

        valorBtc = respuestaBtcJson['data']['quote']['EUR']['price']
        print("VALOR BTC *********: {}". format(valorBtc))

        if respuestaBtcJson['status']['error_code'] != 0:
            return jsonify({'status': 'fail', 'mensaje': respuestaBtcJson['status']['error_message']})

    
            # ETH
        print("**********************")
        print("**********************")
        lista5 = dbManager.consultaMuchasSQL(query5)
        print(lista5)
        saldoFromEth = 0
        for i in range(len(lista5)):
            saldoFromEth += lista5[i]['cantidad_from']
        print("saldoFrom ETH: {}".format(saldoFromEth))

        lista6 = dbManager.consultaMuchasSQL(query6)
        print(lista6)
        saldoToEth = 0
        for i in range(len(lista6)):
            saldoToEth += lista6[i]['cantidad_to']
        print("saldoTo ETH: {}".format(saldoToEth))

        saldoEth = saldoToEth - saldoFromEth
        print("saldo ETH: {}".format(saldoEth))

        url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol=ETH&convert=EUR&CMC_PRO_API_KEY={}'
        
        respuestaEth = requests.get(url.format(saldoBtc, API_KEY_COINMARKET))
        #### GESTIÓN DE ERRORES ####
        print("respuesta Eth *********: {}". format(respuestaEth))
        respuestaEthJson = respuestaEth.json()
        print("respuesta Eth 2 *********: {}". format(respuestaEthJson))

        valorEth = respuestaEthJson['data']['quote']['EUR']['price']
        print("VALOR ETH *********: {}". format(valorEth))

        if respuestaEthJson['status']['error_code'] != 0:
            return jsonify({'status': 'fail', 'mensaje': respuestaEthJson['status']['error_message']})


            # TOTAL
        valorCryptos = valorBtc + valorEth

        # Calculamos el valor actual de la inversión (saldoFromEur + saldoEurosInv + valorCryptos)
        valorActualInv = saldoFromEur + saldoEurosInv + valorCryptos
        

        return jsonify({'status': 'success', 'data': {"invertido": saldoFromEur, "valor_actual": valorActualInv}})
        # return jsonify({'status': 'success', 'data': {"invertido": saldoToEur, "valor_actual": 0}})
    

    except sqlite3.Error as e:
        return jsonify({'status': 'fail', 'mensaje': str(e)})




import sqlite3
import requests
from flask.json import jsonify
from mycrypto import app
from mycrypto.dataaccess import DBmanager
from flask import jsonify, render_template, request, Response
from http import HTTPStatus
from config import API_KEY_COINMARKET


dbManager = DBmanager(app.config.get('DATABASE')) # instancia de la clase DBmanager

monedas = ('EUR', 'BTC', 'ETH')
saldoFromMonedas = {'EUR': 0, 'BTC': 0, 'ETH': 0 }
saldoToMonedas = {'EUR': 0, 'BTC': 0, 'ETH': 0 }
saldoMonedas = {'EUR': 0, 'BTC': 0, 'ETH': 0 }
valorCrypto = {'BTC': 0, 'ETH': 0 }

queryFrom = "SELECT cantidad_from FROM movimientos WHERE moneda_from = ?;"
queryTo = "SELECT cantidad_to FROM movimientos WHERE moneda_to = ?;"


'''def calculaSaldoFrom(query, parametros=[]):
    lista = dbManager.consultaMuchasSQL(query, parametros)
    saldoFrom = 0
    for i in range(len(lista)):
        saldoFrom += lista[i]['cantidad_from']
    return saldoFrom

def calculaSaldoTo(query, parametros=[]):
    lista = dbManager.consultaMuchasSQL(query, parametros)
    saldoTo = 0
    for i in range(len(lista)):
        saldoTo += lista[i]['cantidad_to']
    return saldoTo'''


def calculaSaldoMoneda(moneda):
    
    listaFrom = dbManager.consultaMuchasSQL(queryFrom, [moneda])
    saldoFrom = 0
    for x in range(len(listaFrom)):
        saldoFrom += listaFrom[x]['cantidad_from']
    saldoFromMonedas[moneda] = saldoFrom

    listaTo = dbManager.consultaMuchasSQL(queryTo, [moneda])
    saldoTo = 0
    for y in range(len(listaTo)):
        saldoTo += listaTo[y]['cantidad_to']
    saldoToMonedas[moneda] = saldoTo

    saldoMonedas[moneda] = saldoToMonedas[moneda] - saldoFromMonedas[moneda]

    return saldoMonedas[moneda]


def calculaSaldo():
    for i in range(len(monedas)):
        listaFrom = dbManager.consultaMuchasSQL(queryFrom, [monedas[i]])
        saldoFrom = 0
        for x in range(len(listaFrom)):
            saldoFrom += listaFrom[x]['cantidad_from']
        saldoFromMonedas[monedas[i]] = saldoFrom

        listaTo = dbManager.consultaMuchasSQL(queryTo, [monedas[i]])
        saldoTo = 0
        for y in range(len(listaTo)):
            saldoTo += listaTo[y]['cantidad_to']
        saldoToMonedas[monedas[i]] = saldoTo

        saldoMonedas[monedas[i]] = saldoToMonedas[monedas[i]] - saldoFromMonedas[monedas[i]]

    return saldoFromMonedas, saldoToMonedas, saldoMonedas





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
            print("***** REQUEST JSON ******: {}".format(request.json))

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
    
    
    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert=EUR&CMC_PRO_API_KEY={}'
    

    try:
        
        # Calculamos saldo FROM/TO y el saldo (saldoTo - saldoFrom) de cada moneda
        calculaSaldo()
        print("saldoFrom MONEDAS: {}".format(saldoFromMonedas))
        print("saldoTo MONEDAS: {}".format(saldoToMonedas))
        print("saldo MONEDAS: {}".format(saldoMonedas))
        
        '''for i in range(len(monedas)):
            saldoFromMonedas[monedas[i]] = calculaSaldoFrom(queryFrom, [monedas[i]])
            saldoToMonedas[monedas[i]] = calculaSaldoTo(queryTo, [monedas[i]])
            saldoMonedas[monedas[i]] = saldoToMonedas[monedas[i]] - saldoFromMonedas[monedas[i]]
        print("saldoFrom MONEDAS: {}".format(saldoFromMonedas))
        print("saldoTo MONEDAS: {}".format(saldoToMonedas))
        print("saldo MONEDAS: {}".format(saldoMonedas))'''
        
        # Calculamos el valor en € de nuestras Cryptos
        for i in range(1, len(monedas)):
            if saldoMonedas[monedas[i]] > 0:
                respuestaCrypto = requests.get(url.format(saldoMonedas[monedas[i]], monedas[i], API_KEY_COINMARKET)).json()
                print("respuesta CRYPTO {} *********: {}". format(monedas[i], respuestaCrypto))

                if respuestaCrypto['status']['error_code'] != 0:
                    return jsonify({'status': 'fail', 'mensaje': respuestaCrypto['status']['error_message']})

                valorCrypto[monedas[i]] = respuestaCrypto['data']['quote']['EUR']['price']
                print("VALOR CRYPTO {} *********: {}". format(monedas[i], valorCrypto[monedas[i]]))

        # Calculamos el valor TOTAL en € de todas las Cryptos
        valorCryptosTotal = sum(valorCrypto.values())
        print("VALOR TOTAL CRYPTOS: {}".format(valorCryptosTotal))

        # Calculamos el valor actual de la inversión (saldoFromEur + saldoEurosInv + valorCryptos)
        valorActualInv = saldoToMonedas['EUR'] + valorCryptosTotal
        

        return jsonify({'status': 'success', 'data': {"invertido": saldoFromMonedas['EUR'], "valor_actual": valorActualInv}})
    

    except sqlite3.Error as e:
        return jsonify({'status': 'fail', 'mensaje': str(e)})


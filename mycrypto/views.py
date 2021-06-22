import sqlite3
import requests
from flask.json import jsonify
from mycrypto import app
from mycrypto.dataaccess import DBmanager
from flask import jsonify, render_template, request, Response
from http import HTTPStatus
from config import API_KEY_COINMARKET


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
def statusAPI():
    # Calculamos el total invertido
    # query = "SELECT SUM(cantidad_from) FROM movimientos WHERE moneda_from='EUR';"
    query = "SELECT cantidad_from FROM movimientos WHERE moneda_from='EUR';"

    try:
        lista = dbManager.consultaMuchasSQL(query)
        
        return jsonify({'status': 'success', 'data': lista})
    except sqlite3.Error as e:
        return jsonify({'status': 'fail', 'mensaje': str(e)})

    



    
    

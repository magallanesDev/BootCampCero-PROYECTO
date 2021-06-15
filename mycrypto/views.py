from mycrypto import app
from mycrypto.dataaccess import DBmanager
import sqlite3
from flask.json import jsonify
from flask import jsonify, render_template, request
from http import HTTPStatus

dbManager = DBmanager(app.config.get('DATABASE'))


@app.route('/')
def listaMovimientos():
    return render_template('spa.html')


@app.route('/api/v1/movimientos')
def movimientosAPI():
    query = "SELECT * FROM movimientos ORDER BY fecha;"
    
    try:
        lista = dbManager.consultaMuchasSQL(query)
        return jsonify({'status': 'success', 'movimientos': lista})
    except sqlite3.Error as e:
        return jsonify({'status': 'fail', 'mensaje': str(e)})
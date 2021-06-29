# PROYECTO FINAL del BootCamp Cero VII Ed.

## Aplicación web myCRYPTO - FLASK + VANILLA JS

### Inicio: 14 junio 2021 -- Final: 5 julio 2021

### Instrucciones de INSTALACIÓN:

#### Instalar y activar entorno virtual en PYTHON:
    python -m venv <nombre_entorno_virtual>

    . <nombre_entorno_virtual>/bin/activate

#### Instalar FLASK. Instalar <requirements.txt> y librería <dotenv>:
    pip install Flask

    pip install -r requeriments.txt
    
	pip install python-dotenv

#### Rellenar el archivo <.env_template> con punto de entrada <run.py> y modo de ejecución <development> o <production>. Renombrar el archivo <.env_template> a <.env>

#### Rellenar el archivo <config_template.py> con la ruta a base de datos y la API-KEY de CoinMarketCap. Renombrar el archivo <config_template.py> a <config.py>

#### Crear la base de datos SQL <movimientos.db> en el directorio <data>. Ver archivo </migrations/initial.sql>
    CREATE TABLE "movimientos" (
    "id"	INTEGER,
    "date"	TEXT NOT NULL,
    "time"	TEXT NOT NULL,
    "moneda_from"	TEXT NOT NULL,
    "cantidad_from"	REAL NOT NULL,
    "moneda_to"	TEXT NOT NULL,
    "cantidad_to"	REAL NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
    )

#### Ejecutar FLASK:
    flask run

#### Lanzar aplicación web en el navegador:
	localhost:5000





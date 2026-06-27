import mysql.connector
from flask import g

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '@Darel230109',
    'database': 'pp3_grupo_ad'
}

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**DB_CONFIG)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

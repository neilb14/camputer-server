import sqlite3
from flask import Flask, jsonify, g

DATABASE = "camputer.db"
# instantiate the app
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/ping', methods=['GET'])
def ping_pong():
    results = {
        'status' : 'success',
        'message' : 'pong!',
        'data' : []
    }
    for sample in query_db('select * from samples'):
        results['data'].append(sample[1])
    return jsonify(results)
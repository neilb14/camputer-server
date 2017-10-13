import os, sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy 


db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)
    CORS(app)
    
    if config:
        app.config.from_object(config)
    else:
        app.config.from_object(os.environ['PROJECT_SETTINGS'])
    db.app = app
    db.init_app(app)

    from camputer.views import temperatures_blueprint
    from camputer.views import humidities_blueprint
    app.register_blueprint(temperatures_blueprint)
    app.register_blueprint(humidities_blueprint)

    return app

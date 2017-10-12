from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from camputer.models import Temperature
from camputer.models import Humidity

temperatures_blueprint = Blueprint('temperatures', __name__)

@temperatures_blueprint.route('/temperatures/last', methods=['GET'])
def get_temperatures():
    result = Temperature.query.order_by(Temperature.timestamp.desc()).first()
    return jsonify({
        'timestamp': result.timestamp,
        'uom': 'c',
        'value': result.value
    })

@temperatures_blueprint.route('/temperatures', methods=['GET'])
def get_temperature_range():
    hours = int(request.args.get('hours'))
    results = Temperature.query.filter(Temperature.timestamp >= datetime.utcnow() - timedelta(seconds=hours*60*60)).order_by(Temperature.timestamp.desc()).all()
    readings = []
    for result in results:
        readings.append({
            'timestamp': result.timestamp,
            'uom':'c',
            'value': result.value
        })
    return jsonify({
        'readings': readings,
        'count': len(readings)
    })


humidities_blueprint = Blueprint('humidities', __name__)

@humidities_blueprint.route('/humidities/last', methods=['GET'])
def get_humidities():
    result = Humidity.query.order_by(Humidity.timestamp.desc()).first()
    return jsonify({
        'timestamp': result.timestamp,
        'uom': '%',
        'value': result.value
    })

@humidities_blueprint.route('/humidities', methods=['GET'])
def get_humidity_range():
    hours = int(request.args.get('hours'))
    results = Humidity.query.filter(Humidity.timestamp >= datetime.utcnow() - timedelta(seconds=hours*60*60)).order_by(Humidity.timestamp.desc()).all()
    readings = []
    for result in results:
        readings.append({
            'timestamp': result.timestamp,
            'uom':'%',
            'value': result.value
        })
    return jsonify({
        'readings': readings,
        'count': len(readings)
    })

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from camputer.models.temperature import Temperature
from camputer import db

temperatures_blueprint = Blueprint('temperatures', __name__)

@temperatures_blueprint.route('/temperatures/last', methods=['GET'])
def get_temperatures():
    result = Temperature.query.order_by(Temperature.timestamp.desc()).first()
    return jsonify({
        'id': result.id,
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
            'id': result.id,
            'timestamp': result.timestamp,
            'uom':'c',
            'value': result.value
        })
    return jsonify({
        'readings': readings,
        'count': len(readings)
    })

@temperatures_blueprint.route('/temperatures', methods=['POST'])
def add_temperature_reading():
    post_data = request.get_json()
    if not post_data:
        response_object = {'status': 'fail', 'message':'Invalid payload'}
        return jsonify(response_object), 400
    value = post_data.get('value')
    timestamp = datetime.strptime(post_data.get('timestamp'), '%Y-%m-%dT%H:%M:%S.%f')

    temperature = Temperature(timestamp, value)
    db.session.add(temperature)
    db.session.commit()
    
    return jsonify({
        'status' : 'success',
        'message' : 'created'
    }), 201
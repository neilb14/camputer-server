from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from camputer.models.sensor_reading import SensorReading
from camputer import db

sensor_readings_blueprint = Blueprint('sensor_readings', __name__)

@sensor_readings_blueprint.route('/sensorreadings/last', methods=['GET'])
def get_sensor_readings():
    result = SensorReading.query.order_by(SensorReading.timestamp.desc()).first()
    return jsonify({
        'id': result.id,
        'timestamp': result.timestamp,
        'uom': 'c',
        'value': result.value
    })

@sensor_readings_blueprint.route('/sensorreadings', methods=['GET'])
def get_sensor_reading_range():
    hours = int(request.args.get('hours'))
    results = SensorReading.query.filter(SensorReading.timestamp >= datetime.utcnow() - timedelta(seconds=hours*60*60)).order_by(SensorReading.timestamp.desc()).all()
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

@sensor_readings_blueprint.route('/sensorreadings', methods=['POST'])
def add_sensor_reading_reading():
    post_data = request.get_json()
    if not post_data:
        response_object = {'status': 'fail', 'message':'Invalid payload'}
        return jsonify(response_object), 400
    value = post_data.get('value')
    timestamp = datetime.strptime(post_data.get('timestamp'), '%Y-%m-%dT%H:%M:%S.%f')

    temperature = SensorReading('temperature', timestamp, value)
    db.session.add(temperature)
    db.session.commit()
    
    return jsonify({
        'status' : 'success',
        'message' : 'created'
    }), 201
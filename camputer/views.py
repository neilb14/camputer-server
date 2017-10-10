from flask import Blueprint, jsonify
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

humidities_blueprint = Blueprint('humidities', __name__)

@humidities_blueprint.route('/humidities/last', methods=['GET'])
def get_humidities():
    result = Humidity.query.order_by(Humidity.timestamp.desc()).first()
    return jsonify({
        'timestamp': result.timestamp,
        'uom': '%',
        'value': result.value
    })
from flask import Blueprint, jsonify
from camputer.models import Temperature

temperatures_blueprint = Blueprint('temperatures', __name__)

@temperatures_blueprint.route('/temperatures/last', methods=['GET'])
def get_temperatures():
    result = Temperature.query.order_by(Temperature.timestamp.desc()).first()
    return jsonify({
        'timestamp': result.timestamp,
        'uom': 'c',
        'value': result.value
    })
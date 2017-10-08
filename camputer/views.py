from flask import Blueprint, jsonify

temperatures_blueprint = Blueprint('temperatures', __name__)

@temperatures_blueprint.route('/temperatures', methods=['GET'])
def get_temperatures():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
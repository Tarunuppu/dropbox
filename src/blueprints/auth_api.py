from flask import Blueprint, jsonify, request
from src.services import AuthService


auth_api = Blueprint('auth_api', __name__) # auth_api Blueprint

@auth_api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'invalid payload'}), 400
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    return AuthService.register(name, email, password)

@auth_api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'invalid payload'}), 400
    email = data.get('email')
    password = data.get('password')
    return AuthService.login(email, password)

@auth_api.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'logout'}), 200

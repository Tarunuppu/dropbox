from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

from src.services import DashboardService


dashboard_api = Blueprint('dashboard_api', __name__) # dashboard_api Blueprint


def user_verification(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = DashboardService.check_user(user_id)
        if not user:
            return jsonify({'message': 'unauthorized'}), 401
        return fn(user_id, *args, **kwargs)
    return wrapper



@dashboard_api.route('/list', methods=['GET'])
@user_verification
def list(user_id):
    return DashboardService.list(user_id)



@dashboard_api.route('/upload', methods=['POST'])
@user_verification
def upload(user_id):
    file = request.files.get("file")
    if not file:
        return jsonify({'message': 'invalid payload'}), 400
    
    filename = file.filename
    extension = filename.split('.')[-1]

    if extension not in ['jpg', 'jpeg', 'png', 'pdf', 'docx']:
        return jsonify({'message': 'invalid file type'}), 400
    
    return DashboardService.upload(user_id, file)



@dashboard_api.route('/delete', methods=['DELETE'])
@user_verification
def delete(user_id):
    data = request.get_json()
    if not data or not data.get('file_name'):
        return jsonify({'message': 'invalid payload'}), 400
    return DashboardService.delete(user_id, data.get('file_name'))



@dashboard_api.route('/download', methods=['GET'])
def download():
    return jsonify({'message': 'download'}), 200






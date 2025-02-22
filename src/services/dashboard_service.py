from flask import jsonify

from src.models import User
from src.models import UserFiles
from src.extensions.sqlalchemy import db 
from .s3 import S3

class DashboardService:
    @staticmethod
    def check_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return False
        return True
    
    @staticmethod
    def list(user_id):
        all_files = UserFiles.query.filter_by(user_id=user_id).all()
        return jsonify([file.file_name for file in all_files])

    @staticmethod
    def upload(user_id, file):
        file_name = file.filename
        file_exist = UserFiles.query.filter_by(user_id=user_id, file_name=file_name).first()
        if file_exist:
            base_name, extension = file_name.rsplit('.', 1) if '.' in file_name else (file_name, '')
            count = 1
            while file_exist:
                modified_file_name = f"{base_name}({count}){'.' + extension if extension else ''}"
                file_exist = UserFiles.query.filter_by(user_id=user_id, file_name=modified_file_name).first()
                count += 1
            file_name = modified_file_name

        #uploading file to s3
        s3_client = S3()
        s3_path = f"{user_id}/{file_name}"
        is_uploaded = s3_client.upload(file, s3_path) 
        if not is_uploaded:
            return jsonify({'message': 'internal server error'}), 500
        
        #logging in database
        new_file = UserFiles(user_id, file_name)
        try:
            db.session.add(new_file)
            db.session.commit()
            return DashboardService.list(user_id)
        except Exception as e:
            print(e)
            return jsonify({'message': 'internal server error'}), 500
        


    @staticmethod
    def delete(user_id, file_name):

        file = UserFiles.query.filter_by(user_id=user_id, file_name=file_name).first()
        if not file:
            return jsonify({'message': 'file not found'}), 404
        

        #deleting file from s3
        s3_client = S3()
        is_deleted = s3_client.delete(f"{user_id}/{file_name}")
        if not is_deleted:
            return jsonify({'message': 'internal server error'}), 500
        
        #deleting file from database
        db.session.delete(file)
        db.session.commit()
        return DashboardService.list(user_id)
    

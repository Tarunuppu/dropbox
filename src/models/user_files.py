from src.extensions.sqlalchemy import db
from sqlalchemy import Index, UniqueConstraint

class UserFiles(db.Model):
    __tablename__ = 'user_files'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    file_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, user_id, file_name):
        self.user_id = user_id
        self.file_name = file_name
    
    __table_args__ = (
        UniqueConstraint('user_id', 'file_name', name='uq_user_files_user_id_file_name'),
    )

Index('user_files_user_id_file_name', UserFiles.user_id, UserFiles.file_name)
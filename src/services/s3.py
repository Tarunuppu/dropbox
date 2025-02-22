from src.extensions.s3 import s3
from dotenv import load_dotenv

load_dotenv()
import os

class S3:
    def __init__(self):
        self.s3 = s3
        
    def upload(self, file, file_name):
        try:
            self.s3.upload_fileobj(file, os.getenv('AWS_BUCKET_NAME'), file_name)
            return True
        except Exception as e:
            print(e)
            return False
        
    def delete(self, file_name):
        try:
            self.s3.delete_object(Bucket=os.getenv('AWS_BUCKET_NAME'), Key=file_name)
            return True
        except Exception as e:
            print(e)
            return False

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chqOuYWlwfVDWzqMTyVcTVlnhgAdaPOC'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:chqOuYWlwfVDWzqMTyVcTVlnhgAdaPOC@postgres.railway.internal:5432/railway'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'case_files'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
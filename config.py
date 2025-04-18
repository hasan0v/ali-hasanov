import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    
    # PostgreSQL Database URI
    # Format: postgresql://username:password@hostname/database_name
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # If DATABASE_URL is set in environment, use it; otherwise use SQLite as fallback
    if DATABASE_URL:
        if DATABASE_URL.startswith('postgres://'):
            # Heroku specific fix for SQLAlchemy 1.4+
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
        
        # Replace postgresql:// with postgresql+pg8000:// to use the pg8000 driver
        if DATABASE_URL.startswith('postgresql://'):
            DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+pg8000://')
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application Settings
    APP_NAME = os.environ.get('APP_NAME', 'Ali Hasanov')
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    WTF_CSRF_ENABLED = True
    
    # File Upload Settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload


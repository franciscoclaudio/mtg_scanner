import os
from datetime import timedelta

class Config:
    """Configurações base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    CORS_ORIGINS = ['http://localhost', 'http://127.0.0.1']
    
    # Scryfall API
    SCRYFALL_API_URL = "https://api.scryfall.com"
    SCRYFALL_RATE_LIMIT_DELAY = 0.1  # segundos
    
    # OCR
    TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'temp'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    
    # Cache
    CARD_CACHE_FILE = 'card_cache.json'
    CACHE_TIMEOUT = timedelta(days=7)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

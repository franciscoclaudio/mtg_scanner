from flask import Flask
from flask_cors import CORS
from .utils.config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Extensões
    CORS(app)
    
    # Registrar Blueprints
    from .routes.scanner import scanner_bp
    from .routes.cards import cards_bp
    
    app.register_blueprint(scanner_bp, url_prefix='/api')
    app.register_blueprint(cards_bp, url_prefix='/api/cards')
    
    return app

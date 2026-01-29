from flask import Flask
import openai
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar OpenAI API
    openai.api_key = app.config["OPENAI_API_KEY"]
    
    # Rutas
    from .routes import main
    app.register_blueprint(main)

    return app

from flask import Flask
from ContractorTracker.app.routes import bp  # Adjust the import as necessary

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'

    # Register Blueprints
    app.register_blueprint(bp)

    return app

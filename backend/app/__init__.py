from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Import and register blueprints
from app.endpoints import upload
app.register_blueprint(upload.upload_bp)

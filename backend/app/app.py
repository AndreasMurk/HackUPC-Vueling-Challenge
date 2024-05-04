from flask import Flask
from app.endpoints.upload import upload_bp

# Initialize the Flask application
app = Flask(__name__)

# Configure Flask app settings if needed
# app.config['DEBUG'] = True

# Register blueprints
app.register_blueprint(upload_bp)

# If you have other blueprints, you can register them here

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)

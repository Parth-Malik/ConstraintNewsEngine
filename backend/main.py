import sys
import os
from flask import Flask
from flask_cors import CORS

# Fix imports to ensure the app folder is correctly targeted
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api.routes import api_bp

def create_app():
    app = Flask(__name__)

    # Enable CORS to allow the Next.js frontend to talk to this API
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # Register routes blueprint - Do not use dispatch_request here
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

app = create_app()

if __name__ == "__main__":
    print("🚀 Starting Sigma Backend Server on port 5000...")
    print("   - Neural Interface: http://127.0.0.1:5000")
    
    # Run on 127.0.0.1 to avoid Windows 'localhost' connection refused bugs
    app.run(host="127.0.0.1", port=5000, debug=True)
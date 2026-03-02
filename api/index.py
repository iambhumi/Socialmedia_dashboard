from flask import Flask
from flask_cors import CORS
# Import your Flask app from backend
import sys
sys.path.insert(0, 'backend')
from app import app

CORS(app)

# Vercel recognizes this
app = Flask(__name__)
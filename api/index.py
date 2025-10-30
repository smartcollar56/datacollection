import os
import sys

# Add the api directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app from app.py
from app import app

# This file is required for Vercel deployment
# It exposes the Flask app instance that Vercel will use


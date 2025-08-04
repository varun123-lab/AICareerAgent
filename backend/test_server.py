#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '/Users/varunbarmavat/Desktop/AICareerAgent/backend')

# Set working directory
os.chdir('/Users/varunbarmavat/Desktop/AICareerAgent/backend')

# Import and run the app
from app import app

if __name__ == "__main__":
    print("Starting Flask app on port 5000...")
    app.run(debug=True, host='127.0.0.1', port=5000)

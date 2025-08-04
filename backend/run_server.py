#!/usr/bin/env python3

import subprocess
import sys
import os

# Get current directory
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")

# Check if app.py exists
app_py_path = os.path.join(current_dir, "app.py")
print(f"Looking for app.py at: {app_py_path}")
print(f"app.py exists: {os.path.exists(app_py_path)}")

# List files in current directory
print("\nFiles in current directory:")
for file in os.listdir(current_dir):
    print(f"  {file}")

# Try to run the Flask app
if os.path.exists(app_py_path):
    print(f"\nTrying to run: python3 {app_py_path}")
    try:
        # Import and run the Flask app
        sys.path.insert(0, current_dir)
        import app
        print("Successfully imported app.py")
        print("Starting Flask server...")
        app.app.run(host='127.0.0.1', port=5002, debug=True)
    except Exception as e:
        print(f"Error running app: {e}")
else:
    print("app.py not found!")

#!/bin/bash

# Navigate to the directory where your Flask app is, if needed
# cd path/to/app_directory  # Uncomment and edit if your app isn't in the root

export FLASK_APP=app.py
export FLASK_ENV=development  # Optional: enables debug mode

# Run the Flask app on all interfaces so it's accessible externally, port 5000
flask run 
import os

# Database configuration
DATABASE_URL = "sqlite:///property_management.db"

# Application settings
APP_NAME = "Property Management System"
VERSION = "1.0.0"

# Security settings
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-here")
SESSION_TIMEOUT = 3600  # seconds

# UI settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

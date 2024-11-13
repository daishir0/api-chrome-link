from os import environ
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask Configuration
class Config:
    # Server Settings
    HOST = environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(environ.get('FLASK_PORT', 6000))
    DEBUG = environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

    # Security
    API_KEY = environ.get('API_KEY', 'your-default-key-here')
    
    # Chrome Driver Settings
    CHROME_BINARY_PATH = environ.get('CHROME_BINARY_PATH', '/usr/bin/google-chrome')
    CHROME_DRIVER_PATH = environ.get('CHROME_DRIVER_PATH', '/usr/bin/chromedriver')
    
    # Screenshot Settings
    MAX_SIZE_MB = float(environ.get('MAX_SIZE_MB', 0.5))
    MAX_SIZE_BYTES = int(MAX_SIZE_MB * 1024 * 1024)
    
    # Source Code Settings
    MAX_SRC_SIZE_MB = float(environ.get('MAX_SRC_SIZE_MB', 0.3))
    MAX_SRC_SIZE_BYTES = int(MAX_SRC_SIZE_MB * 1024 * 1024)
    
    # Selenium Settings
    SELENIUM_WAIT_TIME = int(environ.get('SELENIUM_WAIT_TIME', 5))
    WINDOW_WIDTH = int(environ.get('WINDOW_WIDTH', 1920))
    WINDOW_HEIGHT = int(environ.get('WINDOW_HEIGHT', 2160))
    
    # Image Compression Settings
    JPEG_QUALITY = int(environ.get('JPEG_QUALITY', 30))

from flask import Flask, request, jsonify, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import time
import base64
import io
import os
import uuid
import logging
from functools import wraps
from config import Config

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('API-KEY')
        if api_key != Config.API_KEY:
            logger.warning('Invalid API key attempt')
            return jsonify({'error': 'Forbidden'}), 403
        return f(*args, **kwargs)
    return decorated_function

def capture_page_data(url):
    logger.info(f"Starting capture for URL: {url}")
    
    options = Options()
    options.headless = True
    options.binary_location = Config.CHROME_BINARY_PATH
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--enable-logging')
    options.add_argument('--log-level=1')
    options.add_argument("--headless")

    service = Service(executable_path=Config.CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

    try:
        driver.get(url)
        # Wait for page load
        time.sleep(Config.SELENIUM_WAIT_TIME)

        session_id = str(uuid.uuid4())
        screenshot_path = f'temp_screenshot_{session_id}.png'
        compressed_screenshot_path = f'compressed_screenshot_{session_id}.jpg'

        logger.info(f"Taking screenshot: {screenshot_path}")
        driver.save_screenshot(screenshot_path)
        
        page_source = driver.page_source
        logger.info("Page source captured successfully")

        # Compress screenshot
        logger.info("Compressing screenshot")
        with Image.open(screenshot_path) as img:
            img = img.convert("RGB")
            img.save(compressed_screenshot_path, 'JPEG', 
                    optimize=True, quality=Config.JPEG_QUALITY)

        # Read and encode screenshot
        with open(compressed_screenshot_path, 'rb') as img_file:
            screenshot_data = img_file.read()
            if len(screenshot_data) > Config.MAX_SIZE_BYTES:
                logger.error("Screenshot size exceeds maximum limit")
                return {'error': 'Screenshot size exceeds maximum limit'}
            screenshot_base64 = base64.b64encode(screenshot_data).decode('utf-8')

        # Cleanup temporary files
        logger.info("Cleaning up temporary files")
        os.remove(screenshot_path)
        os.remove(compressed_screenshot_path)

        return {
            'screenshot': screenshot_base64,
            'html_source': page_source
        }

    except Exception as e:
        logger.error(f"Error during capture: {str(e)}", exc_info=True)
        raise

    finally:
        driver.quit()
        logger.info("Browser session closed")

@app.route('/get_ss', methods=['POST'])
@require_api_key
def get_screenshot():
    logger.info("Received screenshot request")
    
    url = request.form.get('url')
    if not url:
        logger.warning("No URL provided in request")
        return jsonify({'error': 'URL is required'}), 400

    try:
        result = capture_page_data(url)
        if 'error' in result:
            return jsonify(result), 400

        screenshot_data = base64.b64decode(result['screenshot'])
        logger.info("Successfully processed screenshot")
        
        return send_file(
            io.BytesIO(screenshot_data),
            mimetype='image/jpeg',
            as_attachment=False,
            download_name='screenshot.jpg'
        )
    except Exception as e:
        logger.error(f"Error processing screenshot: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/get_source', methods=['POST'])
@require_api_key
def get_source():
    logger.info("Received source code request")
    
    url = request.form.get('url')
    if not url:
        logger.warning("No URL provided in request")
        return jsonify({'error': 'URL is required'}), 400

    try:
        result = capture_page_data(url)
        if 'error' in result:
            return jsonify(result), 400

        html_source = result['html_source']
        html_bytes = html_source.encode('utf-8')
        
        if len(html_bytes) > Config.MAX_SRC_SIZE_BYTES:
            logger.warning("HTML source size exceeds maximum limit, truncating")
            html_bytes = html_bytes[:Config.MAX_SRC_SIZE_BYTES]
            html_source = html_bytes.decode('utf-8', errors='ignore')

        logger.info("Successfully processed HTML source")
        return jsonify({'html_source': html_source})
    
    except Exception as e:
        logger.error(f"Error processing source: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == "__main__":
    logger.info(f"Starting Flask app on {Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

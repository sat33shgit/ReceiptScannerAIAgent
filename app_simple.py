"""
Minimal Receipt Scanner API for Railway deployment
"""
import os
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Import Google Cloud Vision only when needed
def get_vision_client():
    try:
        from google.cloud import vision
        from google.oauth2 import service_account
        
        # Try environment variable first (Railway)
        if os.environ.get('GOOGLE_CLOUD_KEY_JSON'):
            service_account_info = json.loads(os.environ.get('GOOGLE_CLOUD_KEY_JSON'))
            credentials = service_account.Credentials.from_service_account_info(service_account_info)
            return vision.ImageAnnotatorClient(credentials=credentials)
        
        # Try file-based credentials (local)
        elif os.path.exists("service-account-key.json"):
            credentials = service_account.Credentials.from_service_account_file("service-account-key.json")
            return vision.ImageAnnotatorClient(credentials=credentials)
        
        # Try default credentials
        else:
            return vision.ImageAnnotatorClient()
    except Exception as e:
        logger.error(f"Failed to create Vision client: {str(e)}")
        return None

@app.route('/')
def home():
    return jsonify({
        "service": "Receipt Scanner AI Agent",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "scan": "/api/scan (POST)"
        }
    })

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "Receipt Scanner API",
        "version": "1.0.0"
    })

@app.route('/api/scan', methods=['POST'])
def scan_receipt():
    try:
        # Check for file upload
        if 'receipt_image' not in request.files:
            return jsonify({
                "success": False,
                "error": "No receipt_image file provided"
            }), 400
        
        file = request.files['receipt_image']
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400
        
        # Read image bytes
        image_bytes = file.read()
        if len(image_bytes) == 0:
            return jsonify({
                "success": False,
                "error": "Empty file"
            }), 400
        
        # Get Vision client
        client = get_vision_client()
        if not client:
            return jsonify({
                "success": False,
                "error": "Google Cloud Vision not configured"
            }), 500
        
        # Process image
        from google.cloud import vision
        image = vision.Image(content=image_bytes)
        response = client.text_detection(image=image)
        
        if response.error.message:
            return jsonify({
                "success": False,
                "error": f"Vision API error: {response.error.message}"
            }), 500
        
        # Extract text
        texts = response.text_annotations
        if texts:
            full_text = texts[0].description
        else:
            full_text = ""
        
        # Simple extraction (you can enhance this later)
        result = {
            "success": True,
            "data": {
                "store_name": extract_store_name(full_text),
                "total_amount": extract_total_amount(full_text),
                "date": extract_date(full_text)
            },
            "raw_text": full_text[:200] + "..." if len(full_text) > 200 else full_text
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in scan_receipt: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Processing error: {str(e)}"
        }), 500

def extract_store_name(text):
    """Simple store name extraction"""
    if not text:
        return None
    
    lines = text.split('\n')[:5]  # Check first 5 lines
    for line in lines:
        line = line.strip().upper()
        if 'COSTCO' in line:
            return 'Costco'
        elif 'WALMART' in line:
            return 'Walmart'
        elif 'LONDON DRUGS' in line:
            return 'London Drugs'
        elif 'PHARMASAVE' in line:
            return 'Pharmasave'
        elif 'CANADIAN TIRE' in line:
            return 'Canadian Tire'
    
    return lines[0].strip() if lines else None

def extract_total_amount(text):
    """Simple total amount extraction"""
    import re
    if not text:
        return None
    
    # Look for patterns like $XX.XX or TOTAL $XX.XX
    amount_pattern = r'\$(\d+\.\d{2})'
    matches = re.findall(amount_pattern, text)
    
    if matches:
        # Return the largest amount found
        amounts = [float(match) for match in matches]
        return f"CAD {max(amounts):.2f}"
    
    return None

def extract_date(text):
    """Simple date extraction"""
    import re
    if not text:
        return None
    
    # Look for date patterns
    date_patterns = [
        r'(\d{4}/\d{1,2}/\d{1,2})',
        r'(\d{1,2}/\d{1,2}/\d{4})',
        r'(\d{1,2}/\d{1,2}/\d{2})'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

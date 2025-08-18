"""
Receipt Scanner AI Agent - REST API
==================================

A Flask-based REST API for receipt scanning using Google Cloud Vision OCR.
This API can be called by any application to extract receipt information.

Endpoints:
- GET  /: Web interface for testing
- POST /api/scan: JSON API for receipt scanning
- GET  /api/health: Health check endpoint

Author: Created with GitHub Copilot
Repository: https://github.com/sat33shgit/ReceiptScannerAIAgent
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from google.cloud import vision
import re
from typing import Dict, Optional
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Your existing extraction functions (same as before)
def extract_store_name(text: str) -> Optional[str]:
    known_stores = [
        "COSTCO WHOLESALE", "COSTCO", "WALMART", "SAVE ON FOODS", "HMART", 
        "LONDON DRUGS LIMITED", "LONDON DRUGS", "SUPERSTORE", "PHARMASAVE",
        "CANADIAN TIRE", "TRIANGLE"
    ]
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    for line in lines:
        for store in known_stores:
            if store in line.upper():
                if "LONDON DRUGS" in store:
                    return "London Drugs"
                elif "COSTCO" in store:
                    return "Costco"
                elif "WALMART" in store:
                    return "Walmart"
                elif "SAVE ON FOODS" in store:
                    return "Save On Foods"
                elif "HMART" in store:
                    return "Hmart"
                elif "SUPERSTORE" in store:
                    return "Superstore"
                elif "PHARMASAVE" in store:
                    return "Pharmasave"
                elif "CANADIAN TIRE" in store or "TRIANGLE" in store:
                    return "Canadian Tire"
    
    generic_headers = ["TRANSACTION RECORD", "RECEIPT", "CUSTOMER COPY", "MERCHANT COPY"]
    for line in lines:
        if line.upper() not in generic_headers and len(line.strip()) > 2:
            return line
    
    if lines:
        return lines[0]
    return None

def extract_total_amount(text: str) -> Optional[str]:
    lines = [line for line in text.split('\n') if line.strip()]
    amount_candidates = []
    total_line_amount = None
    
    cad_amount_regex = re.compile(r"(\$|CAD)[ ]?([\d,]+[\.,]\d{2})")
    number_regex = re.compile(r"([\d,]+[\.,]\d{2})")
    
    for line in lines:
        if 'total' in line.lower():
            match = cad_amount_regex.search(line)
            if match:
                total_line_amount = f"CAD {match.group(2).replace(',', '')}"
            else:
                match = number_regex.search(line)
                if match:
                    total_line_amount = f"CAD {match.group(1).replace(',', '')}"
        
        for match in cad_amount_regex.finditer(line):
            amount = float(match.group(2).replace(',', '').replace('$', '').replace('CAD', ''))
            amount_candidates.append(amount)
        
        for match in number_regex.finditer(line):
            try:
                amount = float(match.group(1).replace(',', ''))
                amount_candidates.append(amount)
            except:
                pass
    
    if total_line_amount:
        return total_line_amount
    
    if amount_candidates:
        max_amount = max(amount_candidates)
        return f"CAD {max_amount:.2f}"
    return None

def extract_date(text: str) -> Optional[str]:
    lines = text.split('\n')
    for line in lines:
        timestamp_match = re.search(r'(\d{4})/(\d{1,2})/(\d{1,2})\s+\d{1,2}:\d{2}:\d{2}', line)
        if timestamp_match:
            year, month, day = timestamp_match.groups()
            return f"{year}/{month}/{day}"
        
        short_date_match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{2})\s+\d{1,2}:\d{2}', line)
        if short_date_match:
            month, day, year = short_date_match.groups()
            year_int = int(year)
            if year_int <= 30:
                year_int += 2000
            else:
                year_int += 1900
            return f"{month}/{day}/{year_int}"
    
    date_patterns = [
        r"(\d{4}[-/]\d{1,2}[-/]\d{1,2})",
        r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})",
        r"(\d{1,2}[-/]\d{1,2}[-/]\d{2})"
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group(1)
            if '/' in date_str:
                parts = date_str.split('/')
                if len(parts) == 3 and len(parts[2]) == 2:
                    year = int(parts[2])
                    if year <= 30:
                        year += 2000
                    else:
                        year += 1900
                    date_str = f"{parts[0]}/{parts[1]}/{year}"
            return date_str
    
    return None

def scan_receipt_from_image(image_bytes) -> Dict[str, Optional[str]]:
    try:
        # Initialize Google Cloud Vision client
        # For Railway deployment, check for JSON content in environment variable
        service_account_path = "service-account-key.json"
        
        if os.path.exists(service_account_path):
            # Local development or file-based deployment
            from google.oauth2 import service_account
            credentials = service_account.Credentials.from_service_account_file(service_account_path)
            client = vision.ImageAnnotatorClient(credentials=credentials)
        elif os.environ.get('GOOGLE_CLOUD_KEY_JSON'):
            # Railway deployment with JSON in environment variable
            import json
            from google.oauth2 import service_account
            service_account_info = json.loads(os.environ.get('GOOGLE_CLOUD_KEY_JSON'))
            credentials = service_account.Credentials.from_service_account_info(service_account_info)
            client = vision.ImageAnnotatorClient(credentials=credentials)
        else:
            # Try default credentials (for Google Cloud deployment)
            client = vision.ImageAnnotatorClient()
        
        image = vision.Image(content=image_bytes)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if response.error.message:
            logger.error(f"Google Cloud Vision API error: {response.error.message}")
            return {"error": f"OCR processing failed: {response.error.message}"}
        
        if texts:
            text = texts[0].description
        else:
            text = ""
        
        store_name = extract_store_name(text)
        total_amount = extract_total_amount(text)
        date = extract_date(text)
        
        result = {
            "success": True,
            "data": {
                "store_name": store_name,
                "total_amount": total_amount,
                "date": date
            },
            "raw_text": text[:500] if text else ""  # Limit raw text for API response
        }
        
        logger.info(f"Successfully processed receipt: {store_name}, {total_amount}, {date}")
        return result
        
    except Exception as e:
        logger.error(f"Error processing receipt: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def allowed_file(filename: str) -> bool:
    """Check if uploaded file has an allowed extension."""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Receipt Scanner API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 600px; margin: 0 auto; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { background: #007bff; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px; }
            code { background: #e9ecef; padding: 2px 4px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Receipt Scanner AI Agent API</h1>
            <p>A REST API for receipt scanning using Google Cloud Vision OCR.</p>
            
            <div class="endpoint">
                <h3><span class="method">POST</span> /api/scan</h3>
                <p>Extract store information from receipt image</p>
                <p><strong>Request:</strong> multipart/form-data with 'receipt_image' field</p>
                <p><strong>Supported formats:</strong> JPG, JPEG, PNG</p>
                <p><strong>Max file size:</strong> 10MB</p>
            </div>
            
            <div class="endpoint">
                <h3><span class="method">GET</span> /api/health</h3>
                <p>Health check endpoint</p>
            </div>
            
            <h3>Example Response:</h3>
            <pre><code>{
  "success": true,
  "data": {
    "store_name": "Costco",
    "total_amount": "CAD 45.67",
    "date": "2024/01/15"
  }
}</code></pre>
            
            <p><strong>Repository:</strong> <a href="https://github.com/sat33shgit/ReceiptScannerAIAgent">GitHub</a></p>
        </div>
    </body>
    </html>
    """

@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "service": "Receipt Scanner AI Agent",
        "version": "1.0.0"
    }), 200

@app.route('/api/scan', methods=['POST'])
def scan_receipt_api():
    """
    Scan receipt from uploaded image and extract store information.
    
    Request:
        - Method: POST
        - Content-Type: multipart/form-data
        - File field: 'receipt_image' (JPG, PNG supported)
    
    Response:
        - JSON with extracted information
        - Success: {"success": true, "data": {...}}
        - Error: {"success": false, "error": "error message"}
    """
    if 'receipt_image' not in request.files:
        return jsonify({
            "success": False,
            "error": "No receipt_image file provided. Please upload an image file."
        }), 400
    
    file = request.files['receipt_image']
    
    if file.filename == '':
        return jsonify({
            "success": False,
            "error": "No file selected. Please choose an image file."
        }), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "error": "Invalid file type. Please upload JPG, JPEG, or PNG files only."
        }), 400
    
    try:
        image_bytes = file.read()
        
        if len(image_bytes) == 0:
            return jsonify({
                "success": False,
                "error": "Uploaded file is empty."
            }), 400
        
        if len(image_bytes) > 10 * 1024 * 1024:  # 10MB limit
            return jsonify({
                "success": False,
                "error": "File too large. Maximum size is 10MB."
            }), 400
        
        result = scan_receipt_from_image(image_bytes)
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in /api/scan endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)

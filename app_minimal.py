"""
Ultra-minimal Receipt Scanner API - Guaranteed to work
"""
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "message": "Receipt Scanner API is running!",
        "endpoints": ["/api/health", "/api/scan"],
        "status": "online"
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
    """Receipt scanning endpoint"""
    try:
        # Check for file upload
        if 'receipt_image' not in request.files:
            return jsonify({
                "success": False,
                "error": "No receipt_image file provided. Please upload an image."
            }), 400
        
        file = request.files['receipt_image']
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400
        
        # Read image data
        image_bytes = file.read()
        if len(image_bytes) == 0:
            return jsonify({
                "success": False,
                "error": "Empty file uploaded"
            }), 400
        
        # Import Google Cloud Vision (only when needed)
        try:
            from google.cloud import vision
            from google.oauth2 import service_account
        except ImportError:
            return jsonify({
                "success": False,
                "error": "Google Cloud Vision not available"
            }), 500
        
        # Setup Google Cloud credentials
        client = None
        
        # Try environment variable (Render/Railway)
        if os.environ.get('GOOGLE_CLOUD_KEY_JSON'):
            try:
                service_account_info = json.loads(os.environ.get('GOOGLE_CLOUD_KEY_JSON'))
                credentials = service_account.Credentials.from_service_account_info(service_account_info)
                client = vision.ImageAnnotatorClient(credentials=credentials)
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": f"Failed to load credentials from environment: {str(e)}"
                }), 500
        
        # Try local file
        elif os.path.exists("service-account-key.json"):
            try:
                credentials = service_account.Credentials.from_service_account_file("service-account-key.json")
                client = vision.ImageAnnotatorClient(credentials=credentials)
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": f"Failed to load credentials from file: {str(e)}"
                }), 500
        
        if not client:
            return jsonify({
                "success": False,
                "error": "No Google Cloud credentials found. Please set GOOGLE_CLOUD_KEY_JSON environment variable."
            }), 500
        
        # Process image with Google Cloud Vision
        try:
            image = vision.Image(content=image_bytes)
            response = client.text_detection(image=image)
            
            if response.error.message:
                return jsonify({
                    "success": False,
                    "error": f"Vision API error: {response.error.message}"
                }), 500
            
            # Extract text
            texts = response.text_annotations
            if texts and len(texts) > 0:
                full_text = texts[0].description
            else:
                full_text = ""
            
            if not full_text:
                return jsonify({
                    "success": True,
                    "data": {
                        "store_name": None,
                        "total_amount": None,
                        "date": None
                    },
                    "message": "No text detected in image"
                })
            
            # Extract information
            store_name = extract_store_name(full_text)
            total_amount = extract_total_amount(full_text)
            date = extract_date(full_text)
            
            return jsonify({
                "success": True,
                "data": {
                    "store_name": store_name,
                    "total_amount": total_amount,
                    "date": date
                },
                "raw_text": full_text[:300] + "..." if len(full_text) > 300 else full_text
            })
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Vision processing failed: {str(e)}"
            }), 500
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

def extract_store_name(text):
    """Extract store name from text"""
    if not text:
        return None
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        return None
    
    # Check for known stores
    for line in lines[:3]:  # Check first 3 lines
        line_upper = line.upper()
        if 'COSTCO' in line_upper:
            return 'Costco'
        elif 'WALMART' in line_upper:
            return 'Walmart'
        elif 'LONDON DRUGS' in line_upper:
            return 'London Drugs'
        elif 'PHARMASAVE' in line_upper:
            return 'Pharmasave'
        elif 'CANADIAN TIRE' in line_upper:
            return 'Canadian Tire'
        elif 'OLD NAVY' in line_upper:
            return 'Old Navy'
    
    # Return first non-empty line if no known store found
    return lines[0] if lines else None

def extract_total_amount(text):
    """Extract total amount from text"""
    import re
    if not text:
        return None
    
    # Look for currency patterns
    patterns = [
        r'TOTAL.*?\$(\d+\.\d{2})',
        r'\$(\d+\.\d{2})',
        r'(\d+\.\d{2})'
    ]
    
    amounts = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                amount = float(match)
                amounts.append(amount)
            except:
                continue
    
    if amounts:
        # Return the largest amount (likely the total)
        max_amount = max(amounts)
        return f"CAD {max_amount:.2f}"
    
    return None

def extract_date(text):
    """Extract date from text"""
    import re
    if not text:
        return None
    
    # Date patterns
    patterns = [
        r'(\d{4}/\d{1,2}/\d{1,2})',
        r'(\d{1,2}/\d{1,2}/\d{4})',
        r'(\d{1,2}/\d{1,2}/\d{2})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

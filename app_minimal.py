"""
Ultra-minimal Receipt Scanner API - Guaranteed to work
"""
import os
import json
<<<<<<< HEAD
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
=======
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
>>>>>>> 3ebf50df9e98234098e6ef54e601efbcfe5cc5bc
CORS(app)

@app.route('/')
def home():
<<<<<<< HEAD
    return render_template('index.html')
=======
    return jsonify({
        "message": "Receipt Scanner API is running!",
        "endpoints": ["/api/health", "/api/scan"],
        "status": "online"
    })
>>>>>>> 3ebf50df9e98234098e6ef54e601efbcfe5cc5bc

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
<<<<<<< HEAD
=======
        
>>>>>>> 3ebf50df9e98234098e6ef54e601efbcfe5cc5bc
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
<<<<<<< HEAD
    import re
    if not text:
        lines = []
    else:
        lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        return None
    # Robustly detect 'Hmart' even with OCR errors
    hmart_pattern = re.compile(r'\b[hg][m][a][r][t]\b', re.IGNORECASE)
    for line in lines:
        if hmart_pattern.search(line):
            return 'Hmart'
    # Prioritize 'BC Ferries' if found anywhere (match variations)
    bc_ferries_pattern = re.compile(r'bc\s*ferries', re.IGNORECASE)
    for line in lines:
        if bc_ferries_pattern.search(line):
            return 'BC Ferries'
    # Check for other known stores and keywords in all lines
    for line in lines:
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
        elif 'PETRO-CANADA' in line_upper or 'PETRO CANADA' in line_upper:
            return 'Petro-Canada'
        elif 'SAVE-ON-FOODS' in line_upper or 'SAVE ON FOODS' in line_upper:
            return 'Save-On-Foods'
        elif 'CARTER' in line_upper or 'OSHKOSH' in line_upper:
            return line.strip()
    # Fallback: avoid generic phrases like 'TRANSACTION RECORD'
    for line in lines:
        if line.strip() and line.strip().isupper() and 'TRANSACTION RECORD' not in line.upper():
            return line.strip()
    # Return first non-empty line if no known store found
    return lines[0] if lines else None
    
    # Prioritize 'BC Ferries' if found anywhere (match variations)
    import re
    bc_ferries_pattern = re.compile(r'bc\s*ferries', re.IGNORECASE)
    for line in lines:
        if bc_ferries_pattern.search(line):
            return 'BC Ferries'
    # Check for other known stores and keywords in all lines
    for line in lines:
=======
    if not text:
        return None
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        return None
    
    # Check for known stores
    for line in lines[:3]:  # Check first 3 lines
>>>>>>> 3ebf50df9e98234098e6ef54e601efbcfe5cc5bc
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
<<<<<<< HEAD
        elif 'PETRO-CANADA' in line_upper or 'PETRO CANADA' in line_upper:
            return 'Petro-Canada'
        elif 'SAVE-ON-FOODS' in line_upper or 'SAVE ON FOODS' in line_upper:
            return 'Save-On-Foods'
        elif 'CARTER' in line_upper or 'OSHKOSH' in line_upper:
            return line.strip()
    # Fallback: avoid generic phrases like 'TRANSACTION RECORD'
    for line in lines:
        if line.strip() and line.strip().isupper() and 'TRANSACTION RECORD' not in line.upper():
            return line.strip()
=======
    
>>>>>>> 3ebf50df9e98234098e6ef54e601efbcfe5cc5bc
    # Return first non-empty line if no known store found
    return lines[0] if lines else None

def extract_total_amount(text):
    """Extract total amount from text"""
    import re
    if not text:
        return None
    
<<<<<<< HEAD
    # Specifically extract amount from 'Balance Due' or 'Credit' lines
    import re
    lines = text.split('\n')
    for line in lines:
        if 'balance due' in line.lower():
            match = re.search(r'(\d+\.\d{2})', line)
            if match:
                try:
                    amount = float(match.group(1))
                    return f"CAD {amount:.2f}"
                except:
                    continue
    for line in lines:
        if 'credit' in line.lower():
            match = re.search(r'(\d+\.\d{2})', line)
            if match:
                try:
                    amount = float(match.group(1))
                    return f"CAD {amount:.2f}"
                except:
                    continue
    # Prefer amount from last matching keyword line, fallback to largest
    keywords = ['mastercard', 'paid', 'total', 'amount']
    candidate_amount = None
    for line in lines:
        line_lower = line.lower()
        for kw in keywords:
            if kw in line_lower:
                match = re.search(r'(\d+\.\d{2})', line)
                if match:
                    try:
                        amount = float(match.group(1))
                        candidate_amount = amount
                    except:
                        continue
    if candidate_amount is not None:
        return f"CAD {candidate_amount:.2f}"
    # Fallback: largest amount
    patterns = [
        r'Total Prepaid\s+(\d+\.\d{2})',
        r'TOTAL.*?\$(\d+\.\d{2})',
        r'TOTAL.*?(\d+\.\d{2})',
        r'\$(\d+\.\d{2})',
        r'(\d+\.\d{2})'
    ]
=======
    # Look for currency patterns
    patterns = [
        r'TOTAL.*?\$(\d+\.\d{2})',
        r'\$(\d+\.\d{2})',
        r'(\d+\.\d{2})'
    ]
    
>>>>>>> 3ebf50df9e98234098e6ef54e601efbcfe5cc5bc
    amounts = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                amount = float(match)
                amounts.append(amount)
            except:
                continue
<<<<<<< HEAD
    if amounts:
        max_amount = max(amounts)
        return f"CAD {max_amount:.2f}"
=======
    
    if amounts:
        # Return the largest amount (likely the total)
        max_amount = max(amounts)
        return f"CAD {max_amount:.2f}"
    
>>>>>>> 3ebf50df9e98234098e6ef54e601efbcfe5cc5bc
    return None

def extract_date(text):
    """Extract date from text"""
    import re
    if not text:
        return None
    
<<<<<<< HEAD
    import re
    import datetime
    import calendar
    # Prefer YYYY-MM-DD or YYYY-MM-DD HH:MM
    patterns = [
        r'(\d{4}-\d{2}-\d{2})',
        r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})',
        r'(\d{4}/\d{1,2}/\d{1,2})',
        r'(\d{1,2}/\d{1,2}/\d{4})',
        r'(\d{1,2}/\d{1,2}/\d{2})',
        r'(\d{2} \w{3} \d{4})',  # e.g., 02 Sep 2025
        r'([A-Za-z]{3}\s?\d{1,2}\'\d{2})'  # e.g., Aug31'25 or Aug 31'25
    ]
    # Find all matches for all patterns
    matches = []
    for pattern in patterns:
        matches += re.findall(pattern, text)
    # Filter out suspicious dates (e.g., those with year > 2100 or < 2000, month > 12, day > 31)
    for date_str in matches:
        try:
            # Try to parse YYYY-MM-DD
            if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
                year, month, day = map(int, date_str.split('-'))
                if 2000 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                    return date_str
            # Try to parse YYYY-MM-DD HH:MM
            if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', date_str):
                year, month, day = map(int, date_str.split()[0].split('-'))
                if 2000 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                    return date_str.split()[0]
            # Try to parse YYYY/MM/DD
            if re.match(r'\d{4}/\d{1,2}/\d{1,2}', date_str):
                year, month, day = map(int, date_str.split('/'))
                if 2000 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                    return f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
            # Try to parse MM/DD/YYYY
            if re.match(r'\d{1,2}/\d{1,2}/\d{4}', date_str):
                month, day, year = map(int, date_str.split('/'))
                if 2000 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                    return f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
            # Try to parse MM/DD/YY
            if re.match(r'\d{1,2}/\d{1,2}/\d{2}', date_str):
                month, day, year = map(int, date_str.split('/'))
                year += 2000
                if 2000 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                    return f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
            # Try to parse '02 Sep 2025'
            m = re.match(r'(\d{2}) ([A-Za-z]{3}) (\d{4})', date_str)
            if m:
                day, month_str, year = m.groups()
                month = list(calendar.month_abbr).index(month_str[:3].title())
                year = int(year)
                if 2000 <= year <= 2100 and 1 <= month <= 12 and 1 <= int(day) <= 31:
                    dt = datetime.date(year, month, int(day))
                    return dt.strftime('%Y-%m-%d')
            # Try to parse 'Aug31'25' or 'Aug 31'25'
            m = re.match(r'([A-Za-z]{3})\s?(\d{1,2})\'(\d{2})', date_str)
            if m:
                month_str, day, year = m.groups()
                month = list(calendar.month_abbr).index(month_str[:3].title())
                year = int(year) + 2000
                if 2000 <= year <= 2100 and 1 <= month <= 12 and 1 <= int(day) <= 31:
                    dt = datetime.date(year, month, int(day))
                    return dt.strftime('%Y-%m-%d')
        except:
            continue
    return None

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

=======
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

>>>>>>> 3ebf50df9e98234098e6ef54e601efbcfe5cc5bc
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

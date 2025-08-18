from flask import Flask, request, render_template, jsonify
import os
from google.cloud import vision
import re
from typing import Dict, Optional
import base64
import io
from PIL import Image

app = Flask(__name__)

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
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=image_bytes)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if response.error.message:
            raise Exception(f'{response.error.message}')
        
        if texts:
            text = texts[0].description
        else:
            text = ""
        
        store_name = extract_store_name(text)
        total_amount = extract_total_amount(text)
        date = extract_date(text)
        
        return {
            "store_name": store_name,
            "total_amount": total_amount,
            "date": date
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_receipt():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    image_bytes = file.read()
    results = scan_receipt_from_image(image_bytes)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

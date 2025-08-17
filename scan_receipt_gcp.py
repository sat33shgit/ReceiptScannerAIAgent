import os
from google.cloud import vision
import re
from typing import Dict, Optional

# Set your Google Cloud credentials (you'll need to set this environment variable)
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-key.json'

# Helper function to extract store name: scan entire text for known store names
def extract_store_name(text: str) -> Optional[str]:
    known_stores = [
        "COSTCO WHOLESALE", "COSTCO", "WALMART", "SAVE ON FOODS", "HMART", 
        "LONDON DRUGS LIMITED", "LONDON DRUGS", "SUPERSTORE", "PHARMASAVE",
        "CANADIAN TIRE", "TRIANGLE"
    ]
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # First scan entire text for known store names
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
    
    # fallback: first non-empty line that's not generic text
    generic_headers = ["TRANSACTION RECORD", "RECEIPT", "CUSTOMER COPY", "MERCHANT COPY"]
    for line in lines:
        if line.upper() not in generic_headers and len(line.strip()) > 2:
            return line
    
    # last resort: first non-empty line
    if lines:
        return lines[0]
    return None

# Helper function to extract total amount with CAD (find largest value or last total)
def extract_total_amount(text: str) -> Optional[str]:
    lines = [line for line in text.split('\n') if line.strip()]
    amount_candidates = []
    total_line_amount = None
    # Regex for CAD amounts
    cad_amount_regex = re.compile(r"(\$|CAD)[ ]?([\d,]+[\.,]\d{2})")
    # Regex for numbers that look like totals
    number_regex = re.compile(r"([\d,]+[\.,]\d{2})")
    for line in lines:
        # Prefer lines with 'total'
        if 'total' in line.lower():
            match = cad_amount_regex.search(line)
            if match:
                total_line_amount = f"CAD {match.group(2).replace(',', '')}"
            else:
                match = number_regex.search(line)
                if match:
                    total_line_amount = f"CAD {match.group(1).replace(',', '')}"
        # Collect all CAD values
        for match in cad_amount_regex.finditer(line):
            amount = float(match.group(2).replace(',', '').replace('$', '').replace('CAD', ''))
            amount_candidates.append(amount)
        # Collect all numbers as fallback
        for match in number_regex.finditer(line):
            try:
                amount = float(match.group(1).replace(',', ''))
                amount_candidates.append(amount)
            except:
                pass
    # Use the last total line if found
    if total_line_amount:
        return total_line_amount
    # Otherwise, return the largest amount found
    if amount_candidates:
        max_amount = max(amount_candidates)
        return f"CAD {max_amount:.2f}"
    return None

# Helper function to extract date
def extract_date(text: str) -> Optional[str]:
    # Search for the specific timestamp line and extract just the date part
    lines = text.split('\n')
    for line in lines:
        # Look for lines that contain a timestamp pattern
        timestamp_match = re.search(r'(\d{4})/(\d{1,2})/(\d{1,2})\s+\d{1,2}:\d{2}:\d{2}', line)
        if timestamp_match:
            year, month, day = timestamp_match.groups()
            return f"{year}/{month}/{day}"
        
        # Also check for M/D/YY format with time
        short_date_match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{2})\s+\d{1,2}:\d{2}', line)
        if short_date_match:
            month, day, year = short_date_match.groups()
            year_int = int(year)
            if year_int <= 30:
                year_int += 2000
            else:
                year_int += 1900
            return f"{month}/{day}/{year_int}"
    
    # Fallback to simpler patterns if no timestamp found
    date_patterns = [
        r"(\d{4}[-/]\d{1,2}[-/]\d{1,2})",  # YYYY-M-D or YYYY/M/D
        r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})",  # M/D/YYYY
        r"(\d{1,2}[-/]\d{1,2}[-/]\d{2})"   # M/D/YY
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group(1)
            # Convert 2-digit year if needed
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

def scan_receipt_gcp(image_path: str) -> Dict[str, Optional[str]]:
    try:
        # Initialize the Google Cloud Vision client
        print("Initializing Google Cloud Vision client...")
        client = vision.ImageAnnotatorClient()
        
        # Load the image
        print(f"Loading image: {image_path}")
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        
        # Perform text detection
        print("Performing text detection...")
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if response.error.message:
            raise Exception(f'{response.error.message}')
            
    except Exception as e:
        print(f"Error: {e}")
        return {"store_name": None, "total_amount": None, "date": None}
    
    # Get the full text
    if texts:
        text = texts[0].description
    else:
        text = ""
    
    # Extract fields
    store_name = extract_store_name(text)
    total_amount = extract_total_amount(text)
    date = extract_date(text)
    
    return {
        "store_name": store_name,
        "total_amount": total_amount,
        "date": date
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python scan_receipt_gcp.py <image_path>")
        sys.exit(1)
    result = scan_receipt_gcp(sys.argv[1])
    print(result)

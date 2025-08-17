import pytesseract
# Explicitly set the tesseract executable path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
from PIL import Image
import cv2
import re
from typing import Dict, Optional


# Helper function to extract store name: scan first 5 lines for known store names
def extract_store_name(text: str) -> Optional[str]:
    known_stores = [
        "COSTCO WHOLESALE", "COSTCO", "WALMART", "SAVE ON FOODS", "HMART", "LONDON DRUGS", "SUPERSTORE"
    ]
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    # Scan first 5 lines for known store names
    for line in lines[:5]:
        for store in known_stores:
            if store in line.upper():
                return store.title()
    # fallback: first non-empty line
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
    # Common date patterns: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY
    date_patterns = [
        r"(\d{4}[-/]\d{2}[-/]\d{2})",
        r"(\d{2}[-/]\d{2}[-/]\d{4})",
        r"(\d{2}[-/]\d{2}[-/]\d{2,4})"
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None

def scan_receipt(image_path: str) -> Dict[str, Optional[str]]:
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Optional: thresholding for better OCR
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    # OCR
    text = pytesseract.image_to_string(Image.fromarray(thresh))
    # Debug: print OCR text
    print("----- OCR TEXT START -----")
    print(text)
    print("----- OCR TEXT END -----")
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
        print("Usage: python scan_receipt.py <image_path>")
        sys.exit(1)
    result = scan_receipt(sys.argv[1])
    print(result)

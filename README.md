# Receipt Scanner AI Agent

An AI-powered receipt scanner that extracts key information from receipt images using Google Cloud Vision OCR.

## Features

- **Store Name Extraction**: Identifies the store name from receipt headers
- **Total Amount Extraction**: Finds the total amount with CAD currency
- **Date Extraction**: Extracts receipt date in various formats
- **Multi-Store Support**: Supports Costco, Walmart, Save On Foods, London Drugs, Hmart, Superstore, and more

## Prerequisites

1. **Python 3.7+**
2. **Google Cloud Vision API**: 
   - Create a Google Cloud project
   - Enable Cloud Vision API
   - Create a service account and download the JSON key
3. **Required Python packages** (see requirements.txt)

## Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd RecieptScanner
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Cloud credentials:
   - Download your service account JSON key file
   - Save it as `service-account-key.json` in the project directory
   - Set the environment variable:
     ```cmd
     set GOOGLE_APPLICATION_CREDENTIALS=c:\path\to\your\project\service-account-key.json
     ```

## Usage

Run the scanner on a receipt image:

```bash
python scan_receipt_gcp.py <image_path>
```

Example:
```bash
python scan_receipt_gcp.py Costco_1.jpg
```

### Sample Output:
```json
{
  "store_name": "Costco", 
  "total_amount": "CAD 192.86", 
  "date": "2025/08/11"
}
```

## Supported Receipt Formats

- **Store Names**: Costco, Walmart, Save On Foods, London Drugs, Hmart, Superstore
- **Date Formats**: YYYY/MM/DD, M/D/YY, MM/DD/YYYY
- **Currency**: CAD (Canadian Dollar)

## Files

- `scan_receipt_gcp.py` - Main scanner using Google Cloud Vision OCR
- `scan_receipt.py` - Legacy scanner using Tesseract (less accurate)
- `requirements.txt` - Python dependencies
- `service-account-key.json` - Google Cloud credentials (not included in repo)

## Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable the Cloud Vision API
4. Create a service account with Editor role
5. Download the JSON key file

## License

This project is open source and available under the MIT License.

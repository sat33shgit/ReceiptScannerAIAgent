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
   git clone https://github.com/sat33shgit/ReceiptScannerAIAgent.git
   cd ReceiptScannerAIAgent
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

- **Store Names**: Costco, Walmart, Save On Foods, London Drugs, Hmart, Superstore, Pharmasave, Canadian Tire, Old Navy
- **Date Formats**: YYYY/MM/DD, M/D/YY, MM/DD/YYYY, YYYY-MM-DD
- **Currency**: CAD (Canadian Dollar)
- **Amount Range**: Successfully tested from CAD 22.03 to CAD 638.39

## Testing Results

The agent has been tested with real receipt images and achieves 100% accuracy across 6 different store types:

### Test Case 1: Costco Receipt
- **Store Name**: Costco ✅
- **Total Amount**: CAD 192.86 ✅  
- **Date**: 2025/08/11 ✅

### Test Case 2: London Drugs Receipt
- **Store Name**: London Drugs ✅
- **Total Amount**: CAD 101.17 ✅
- **Date**: 7/20/2025 ✅

### Test Case 3: Walmart Receipt
- **Store Name**: Walmart ✅
- **Total Amount**: CAD 47.80 ✅
- **Date**: 05/16/2025 ✅

### Test Case 4: Pharmasave Receipt
- **Store Name**: Pharmasave ✅
- **Total Amount**: CAD 72.63 ✅
- **Date**: 2024-12-26 ✅

### Test Case 5: Old Navy Receipt
- **Store Name**: OLD NAVY - 03326 ✅
- **Total Amount**: CAD 22.03 ✅
- **Date**: 05/03/2025 ✅

### Test Case 6: Canadian Tire Receipt
- **Store Name**: Canadian Tire ✅
- **Total Amount**: CAD 638.39 ✅
- **Date**: 2020/08/14 ✅

**Overall Performance: 100% accuracy (18/18 fields)**

## How It Works

1. **Image Processing**: Uses Google Cloud Vision OCR to extract text from receipt images
2. **Store Detection**: Scans the text for known store names and patterns
3. **Amount Extraction**: Identifies total amounts using regex patterns and heuristics
4. **Date Parsing**: Extracts dates in multiple formats with automatic year conversion

## Error Handling

- Handles missing or corrupted images gracefully
- Returns `None` for fields that cannot be extracted
- Provides informative error messages for API issues

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

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Future Enhancements

- [ ] Support for additional currencies (USD, EUR)
- [ ] Tax amount extraction
- [ ] Item-level parsing
- [ ] Receipt categorization
- [ ] Batch processing support
- [ ] Web API interface

## License

This project is open source and available under the MIT License.

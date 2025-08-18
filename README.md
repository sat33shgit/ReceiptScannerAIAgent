# Receipt Scanner AI Agent 🧾

An AI-powered receipt scanner that extracts key information from receipt images using Google Cloud Vision OCR. Available as both a web application and REST API for integration with other applications.

## 🌐 **Live Deployments**
🔗 **Web App**: [Receipt Scanner AI Agent](https://receiptscanneraiagent.streamlit.app/)  
🔗 **REST API**: [https://receipt-scanner-api-lim0.onrender.com](https://receipt-scanner-api-lim0.onrender.com)  
📋 **API Health Check**: [https://receipt-scanner-api-lim0.onrender.com/health](https://receipt-scanner-api-lim0.onrender.com/health)

## ✨ **Features**

- 🏪 **Store Name Extraction**: Automatically identifies store names
- 💰 **Total Amount Extraction**: Finds total amounts in CAD currency  
- 📅 **Date Extraction**: Extracts receipt dates in various formats
- 🏬 **Multi-Store Support**: Costco, Walmart, London Drugs, Pharmasave, Canadian Tire, Old Navy, and more
- 📱 **Mobile-Friendly**: Works on phones, tablets, and computers
- ☁️ **Cloud-Deployed**: Access from anywhere with internet
- 🔗 **REST API**: Production-ready API with CORS support and comprehensive error handling
- ⚡ **100% Accuracy**: Tested across 6+ major store types
- 🚀 **Multiple Deployment Options**: Streamlit web app and standalone Flask API

## 🚀 **Quick Start**

### Option 1: Use the Live Web App (Recommended for End Users)
1. Visit [Receipt Scanner AI Agent](https://receiptscanneraiagent.streamlit.app/)
2. Upload a receipt image (JPG, JPEG, PNG)
3. Get instant results!

### Option 2: Use the REST API (For Developers/Apps)

**API Base URL**: `https://receipt-scanner-api-lim0.onrender.com`

#### Available Endpoints:
- `GET /` - API documentation and endpoint list
- `GET /health` - Health check endpoint
- `POST /api/scan` - Receipt scanning endpoint

#### Example Usage:
```python
import requests

# Health check
response = requests.get('https://receipt-scanner-api-lim0.onrender.com/health')
print(response.json())
# Output: {"status": "healthy", "service": "Receipt Scanner API", "version": "1.0.0"}

# Scan receipt
with open('receipt.jpg', 'rb') as image_file:
    files = {'receipt_image': image_file}
    response = requests.post('https://receipt-scanner-api-lim0.onrender.com/api/scan', files=files)
    result = response.json()

if result.get('success'):
    data = result.get('data')
    print(f"Store: {data['store_name']}")
    print(f"Amount: {data['total_amount']}")
    print(f"Date: {data['date']}")
```

#### cURL Example:
```bash
# Health check
curl https://receipt-scanner-api-lim0.onrender.com/health

# Upload receipt
curl -X POST https://receipt-scanner-api-lim0.onrender.com/api/scan \
  -F "receipt_image=@path/to/your/receipt.jpg"
```

### Option 3: Run Locally

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

## 🛠️ **Project Structure**

```
RecieptScanner/
├── streamlit_app.py               # Main Streamlit web application
├── app.py                         # Flask REST API application
├── app_minimal.py                 # Simplified Flask app for deployment
├── app_simple.py                  # Alternative simplified Flask app
├── scan_receipt_gcp.py            # Core OCR scanning logic
├── test_deployed_api.py           # API testing script
├── test_api.py                    # Local API testing script
├── requirements.txt               # Python dependencies
├── service-account-key.json       # Google Cloud credentials (not in repo)
├── Procfile                       # Render deployment configuration
├── runtime.txt                    # Python version specification
├── render.yaml                    # Render deployment configuration
├── templates/
│   └── index.html                 # Flask app HTML template
├── .streamlit/                    # Streamlit configuration
└── *.jpg                          # Sample receipt images
```

## 🌐 **Deployment Architecture**

- **Web App**: Deployed on Streamlit Cloud for easy user access and interactive UI
- **REST API**: Deployed on Render with auto-scaling, health monitoring, and free tier hosting
- **OCR Engine**: Google Cloud Vision API for high-accuracy text extraction
- **CORS Support**: API configured for cross-origin requests from web applications

## 💻 **Local Development**

### Running the CLI Scanner
```bash
python scan_receipt_gcp.py <image_path>
```

Example:
```bash
python scan_receipt_gcp.py Costco_1.jpg
```

### Running the Flask API Locally
```bash
# Start the API server
python app.py

# The API will be available at http://localhost:5000
```

### Running the Streamlit App Locally
```bash
# Start the web app
streamlit run streamlit_app.py

# The app will open in your browser at http://localhost:8501
```

## 🧪 **API Testing**

Use the included test script to verify API functionality:

```bash
python test_deployed_api.py
```

This script tests:
- Health check endpoint
- Home page endpoint  
- Receipt scanning functionality

## 📊 **API Response Format**

### Successful Response:
```json
{
  "success": true,
  "data": {
    "store_name": "Costco",
    "total_amount": "CAD 192.86", 
    "date": "2025/08/11"
  },
  "message": "Receipt processed successfully"
}
```

### Error Response:
```json
{
  "success": false,
  "error": "Error message details",
  "message": "Failed to process receipt"
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

## 📁 **Key Files**

### Core Application Files
- `streamlit_app.py` - Main interactive web application with file upload UI
- `app.py` - Production Flask REST API with comprehensive error handling
- `app_minimal.py` - Simplified Flask API optimized for cloud deployment
- `app_simple.py` - Alternative simplified Flask API version
- `scan_receipt_gcp.py` - Core OCR scanning logic using Google Cloud Vision
- `test_deployed_api.py` - Automated testing script for deployed API
- `test_api.py` - Local API testing script

### Configuration Files
- `requirements.txt` - Python dependencies for deployment
- `Procfile` - Render deployment configuration
- `render.yaml` - Render deployment configuration file
- `runtime.txt` - Python version specification
- `service-account-key.json` - Google Cloud credentials (excluded from repo)

### UI Files
- `templates/index.html` - HTML template for Flask web interface

### Legacy Files
- `scan_receipt.py` - Legacy scanner using Tesseract (less accurate)

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

## 🔮 **Future Enhancements**

- [ ] Support for additional currencies (USD, EUR)
- [ ] Tax amount extraction
- [ ] Item-level parsing with line items
- [ ] Receipt categorization (grocery, retail, etc.)
- [ ] Batch processing support for multiple receipts
- [ ] Database integration for receipt storage
- [ ] User authentication and receipt history
- [ ] Email integration for receipt forwarding
- [ ] Mobile app development (iOS/Android)
- [ ] Receipt analytics and spending insights

## 📈 **Recent Updates**

- ✅ **v1.0.0**: Production-ready REST API deployed on Render
- ✅ **Enhanced Error Handling**: Comprehensive error responses and logging
- ✅ **CORS Support**: API accessible from web applications
- ✅ **Health Monitoring**: Built-in health check endpoints
- ✅ **Cloud Deployment**: Both Streamlit and Flask apps in production
- ✅ **Automated Testing**: Test suite for API validation

## License

This project is open source and available under the MIT License.

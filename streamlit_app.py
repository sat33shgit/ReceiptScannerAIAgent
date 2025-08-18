"""
Receipt Scanner AI Agent
========================

A Streamlit web application that uses Google Cloud Vision API to extract:
- Store name
- Total amount (CAD)
- Receipt date

From uploaded receipt images.

Author: Created with GitHub Copilot
Repository: https://github.com/sat33shgit/ReceiptScannerAIAgent
"""

import streamlit as st
import os
from google.cloud import vision
import re
from typing import Dict, Optional
from PIL import Image

# Set page config
st.set_page_config(
    page_title="Receipt Scanner AI Agent",
    page_icon="🧾",
    layout="wide"
)

# Helper functions (same as your main script)
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
        # Try local file first, then environment variable, then Streamlit secrets
        client = None
        
        # First priority: Local service account file
        service_account_path = "service-account-key.json"
        if os.path.exists(service_account_path):
            try:
                from google.oauth2 import service_account
                
                # Load service account from local file
                credentials = service_account.Credentials.from_service_account_file(
                    service_account_path
                )
                client = vision.ImageAnnotatorClient(credentials=credentials)
            except Exception as e:
                return {"error": f"Error loading local service account file: {str(e)}"}
        
        # Second priority: Environment variable
        elif os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
            try:
                client = vision.ImageAnnotatorClient()
            except Exception as e:
                return {"error": f"Error with environment variable credentials: {str(e)}"}
        
        # Third priority: Streamlit Cloud secrets
        elif hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
            try:
                from google.oauth2 import service_account
                
                # Create credentials from Streamlit secrets
                gcp_service_account = st.secrets["gcp_service_account"]
                credentials = service_account.Credentials.from_service_account_info(
                    gcp_service_account
                )
                client = vision.ImageAnnotatorClient(credentials=credentials)
            except Exception as e:
                return {"error": f"Invalid Streamlit secrets configuration: {str(e)}"}
        
        else:
            return {"error": "No Google Cloud credentials found. Please ensure service-account-key.json exists in the project directory."}
        
        # Create image object
        image = vision.Image(content=image_bytes)
        
        # Perform text detection
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if response.error.message:
            return {"error": f"Google Cloud Vision API error: {response.error.message}"}
        
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
            "date": date,
            "raw_text": text
        }
        
    except Exception as e:
        return {"error": str(e)}

# Streamlit UI
def main():
    st.title("🧾 Receipt Scanner AI Agent")
    st.markdown("Upload a receipt image to extract store name, total amount, and date")
    
    # Sidebar with info
    with st.sidebar:
        st.header("📊 Supported Stores")
        st.write("✅ Costco")
        st.write("✅ Walmart") 
        st.write("✅ London Drugs")
        st.write("✅ Pharmasave")
        st.write("✅ Canadian Tire")
        st.write("✅ Old Navy")
        st.write("✅ Save On Foods")
        st.write("✅ Hmart")
        st.write("✅ Superstore")
        
        st.header("📅 Date Formats")
        st.write("• YYYY/MM/DD")
        st.write("• MM/DD/YYYY") 
        st.write("• M/D/YY")
        st.write("• YYYY-MM-DD")
        
        st.header("💰 Currency")
        st.write("CAD (Canadian Dollar)")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a receipt image", 
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of your receipt"
    )
    
    if uploaded_file is not None:
        # Display the image
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Uploaded Receipt")
            image = Image.open(uploaded_file)
            st.image(image, caption="Receipt Image", use_container_width=True)
        
        with col2:
            st.subheader("🤖 Extraction Results")
            
            # Process the image
            with st.spinner("Processing receipt..."):
                image_bytes = uploaded_file.getvalue()
                results = scan_receipt_from_image(image_bytes)
            
            if "error" in results:
                st.error(f"❌ Error: {results['error']}")
                
                # Show helpful setup instructions
                st.markdown("### 🔧 Setup Instructions")
                st.markdown("""
                **For Local Testing (Current Setup):**
                ✅ **Good News**: Your `service-account-key.json` file is detected in the project directory!
                
                The app should automatically use this file. If you're still seeing errors:
                
                1. **Option 1**: Restart the Streamlit app completely:
                   ```
                   Ctrl+C to stop the app, then restart with:
                   streamlit run streamlit_app.py
                   ```
                
                2. **Option 2**: Set environment variable manually:
                   ```
                   set GOOGLE_APPLICATION_CREDENTIALS=c:\\Sateesh\\Projects\\RecieptScanner\\service-account-key.json
                   ```
                
                **For Streamlit Cloud Deployment:**
                1. Go to your app settings on Streamlit Cloud
                2. Navigate to the "Secrets" section  
                3. Add your complete Google Cloud service account JSON content in this format:
                   ```toml
                   [gcp_service_account]
                   type = "service_account"
                   project_id = "your-project-id"
                   private_key_id = "your-private-key-id"
                   private_key = "-----BEGIN PRIVATE KEY-----\\nYour private key here\\n-----END PRIVATE KEY-----\\n"
                   client_email = "your-service-account@project.iam.gserviceaccount.com"
                   client_id = "your-client-id"
                   auth_uri = "https://accounts.google.com/o/oauth2/auth"
                   token_uri = "https://oauth2.googleapis.com/token"
                   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
                   client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40project.iam.gserviceaccount.com"
                   ```
                   
                **Troubleshooting:**
                - Ensure your service account has "Cloud Vision API User" permissions
                - Verify the JSON file is not corrupted
                - Check that the Google Cloud Vision API is enabled in your project
                """)
            else:
                # Display results in a nice format
                st.success("✅ Receipt processed successfully!")
                
                # Results cards
                if results["store_name"]:
                    st.metric("🏪 Store Name", results["store_name"])
                else:
                    st.warning("Store name not detected")
                
                if results["total_amount"]:
                    st.metric("💰 Total Amount", results["total_amount"])
                else:
                    st.warning("Total amount not detected")
                
                if results["date"]:
                    st.metric("📅 Date", results["date"])
                else:
                    st.warning("Date not detected")
                
                # JSON output
                st.subheader("📋 JSON Output")
                st.json({
                    "store_name": results["store_name"],
                    "total_amount": results["total_amount"], 
                    "date": results["date"]
                })
                
                # Raw text (expandable)
                with st.expander("🔍 Raw OCR Text"):
                    st.text(results["raw_text"])

if __name__ == "__main__":
    main()

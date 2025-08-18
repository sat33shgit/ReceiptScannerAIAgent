# Google Cloud Run Deployment - Quick Start Commands

## After installing Google Cloud CLI, run these commands:

# 1. Login to Google Cloud
gcloud auth login

# 2. Set your project (replace YOUR_PROJECT_ID with your actual project ID)
gcloud config set project YOUR_PROJECT_ID

# 3. Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable vision.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# 4. Deploy your API (run from your project directory)
cd c:\Sateesh\Projects\RecieptScanner

gcloud run deploy receipt-scanner-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300

## Alternative: Use the batch file (Windows)
# Just double-click: deploy-to-cloudrun.bat

## After deployment, test your API:
# Health check: curl https://YOUR_API_URL/api/health
# Receipt scan: curl -X POST https://YOUR_API_URL/api/scan -F "receipt_image=@receipt.jpg"

## Monitor your service:
# View logs: gcloud run services logs tail receipt-scanner-api --region us-central1
# Cloud Console: https://console.cloud.google.com/run

#!/bin/bash

# Receipt Scanner API - Google Cloud Run Deployment Script
# Run this script to deploy your API to Google Cloud Run

echo "🚀 Deploying Receipt Scanner API to Google Cloud Run..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Google Cloud CLI is not installed.${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ No Google Cloud project is set.${NC}"
    echo "Please run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo -e "${GREEN}✅ Using Google Cloud Project: $PROJECT_ID${NC}"

# Check if required APIs are enabled
echo -e "${YELLOW}🔧 Enabling required APIs...${NC}"
gcloud services enable run.googleapis.com
gcloud services enable vision.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Deploy to Cloud Run
echo -e "${YELLOW}🚀 Deploying to Cloud Run...${NC}"
gcloud run deploy receipt-scanner-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300 \
  --set-env-vars GOOGLE_APPLICATION_CREDENTIALS=service-account-key.json

# Check if deployment was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    
    # Get the service URL
    SERVICE_URL=$(gcloud run services describe receipt-scanner-api --region us-central1 --format 'value(status.url)')
    
    echo -e "${GREEN}🌐 Your API is now live at: $SERVICE_URL${NC}"
    echo ""
    echo -e "${YELLOW}📋 Test your API:${NC}"
    echo "Health check: curl $SERVICE_URL/api/health"
    echo "Upload receipt: curl -X POST $SERVICE_URL/api/scan -F \"receipt_image=@your-receipt.jpg\""
    echo ""
    echo -e "${YELLOW}📊 Monitor your service:${NC}"
    echo "Logs: gcloud run services logs tail receipt-scanner-api --region us-central1"
    echo "Console: https://console.cloud.google.com/run/detail/us-central1/receipt-scanner-api"
    
else
    echo -e "${RED}❌ Deployment failed. Check the error messages above.${NC}"
    exit 1
fi

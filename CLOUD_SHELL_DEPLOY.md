# Google Cloud Shell Deployment Commands
# Copy and paste these commands one by one in Cloud Shell

# 1. Navigate to your project (if you cloned from GitHub)
cd ReceiptScannerAIAgent

# OR if you uploaded files manually:
# mkdir receipt-scanner && cd receipt-scanner
# (then upload your files to this directory)

# 2. FIRST: Check your current project and billing
gcloud config get-value project
gcloud beta billing accounts list

# 3. IMPORTANT: Enable billing for your project
# Go to: https://console.cloud.google.com/billing
# Link a billing account to your project (even free tier requires this)

# 4. After enabling billing, verify project setup:
gcloud config set project 281601491527
gcloud config get-value project

# 5. Enable required APIs (ONLY AFTER billing is enabled)
gcloud services enable run.googleapis.com --project=281601491527
gcloud services enable vision.googleapis.com --project=281601491527
gcloud services enable cloudbuild.googleapis.com --project=281601491527

# 4. Deploy to Cloud Run
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

# 5. Get your API URL
gcloud run services describe receipt-scanner-api \
  --region us-central1 \
  --format 'value(status.url)'

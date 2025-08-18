@echo off
REM Receipt Scanner API - Google Cloud Run Deployment Script for Windows
REM Run this script to deploy your API to Google Cloud Run

echo 🚀 Deploying Receipt Scanner API to Google Cloud Run...

REM Check if gcloud is installed
gcloud --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Google Cloud CLI is not installed.
    echo Please install it from: https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

REM Get project ID
for /f "tokens=*" %%i in ('gcloud config get-value project 2^>nul') do set PROJECT_ID=%%i

if "%PROJECT_ID%"=="" (
    echo ❌ No Google Cloud project is set.
    echo Please run: gcloud config set project YOUR_PROJECT_ID
    pause
    exit /b 1
)

echo ✅ Using Google Cloud Project: %PROJECT_ID%

REM Enable required APIs
echo 🔧 Enabling required APIs...
gcloud services enable run.googleapis.com
gcloud services enable vision.googleapis.com
gcloud services enable cloudbuild.googleapis.com

REM Deploy to Cloud Run
echo 🚀 Deploying to Cloud Run...
gcloud run deploy receipt-scanner-api ^
  --source . ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --port 8080 ^
  --memory 1Gi ^
  --cpu 1 ^
  --max-instances 10 ^
  --timeout 300 ^
  --set-env-vars GOOGLE_APPLICATION_CREDENTIALS=service-account-key.json

if errorlevel 1 (
    echo ❌ Deployment failed. Check the error messages above.
    pause
    exit /b 1
)

echo ✅ Deployment successful!

REM Get the service URL
for /f "tokens=*" %%i in ('gcloud run services describe receipt-scanner-api --region us-central1 --format "value(status.url)"') do set SERVICE_URL=%%i

echo.
echo 🌐 Your API is now live at: %SERVICE_URL%
echo.
echo 📋 Test your API:
echo Health check: curl %SERVICE_URL%/api/health
echo Upload receipt: curl -X POST %SERVICE_URL%/api/scan -F "receipt_image=@your-receipt.jpg"
echo.
echo 📊 Monitor your service:
echo Logs: gcloud run services logs tail receipt-scanner-api --region us-central1
echo Console: https://console.cloud.google.com/run/detail/us-central1/receipt-scanner-api
echo.
pause

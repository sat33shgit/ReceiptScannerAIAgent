# Railway Deployment Instructions

## Deploy Receipt Scanner API to Railway (Free)

### Step 1: Prepare for Deployment

1. **Create railway.json** (Railway configuration):
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

2. **Create Procfile** (Alternative start command):
```
web: gunicorn --bind 0.0.0.0:$PORT app:app
```

### Step 2: Deploy to Railway

1. **Visit Railway**: Go to [railway.app](https://railway.app)

2. **Sign up/Login**: Use your GitHub account

3. **Create New Project**: 
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `ReceiptScannerAIAgent` repository

4. **Set Environment Variables**:
   - Go to your project → Variables tab
   - Add: `GOOGLE_APPLICATION_CREDENTIALS` = `service-account-key.json`
   - Upload your `service-account-key.json` file

5. **Deploy**: Railway will automatically build and deploy!

### Step 3: Test Your Deployed API

Your API will be available at: `https://your-app-name.railway.app`

Test endpoints:
- Health: `https://your-app-name.railway.app/api/health`
- Scan: `https://your-app-name.railway.app/api/scan` (POST with image)

### Alternative: Google Cloud Run (Also Free)

If you prefer Google Cloud Run:

```bash
# Install Google Cloud CLI first
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Deploy
gcloud run deploy receipt-scanner-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

### Cost Monitoring

**Railway**: Check usage at railway.app/dashboard
**Google Cloud Run**: Check at console.cloud.google.com/run

Both platforms will alert you before any charges occur.

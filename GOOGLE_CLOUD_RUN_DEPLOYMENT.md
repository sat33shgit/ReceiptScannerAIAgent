# Deploy Receipt Scanner API to Google Cloud Run

## Prerequisites
- Google Cloud account
- Google Cloud CLI installed
- Your service account key (`service-account-key.json`)

## Step 1: Install Google Cloud CLI

### Windows:
Download and install from: https://cloud.google.com/sdk/docs/install

### Verify Installation:
```bash
gcloud --version
```

## Step 2: Setup Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Set your project (replace with your actual project ID)
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable vision.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

## Step 3: Create Dockerfile (if not exists)

Create `Dockerfile` in your project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a non-root user
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "app:app"]
```

## Step 4: Deploy to Cloud Run

### Option 1: Deploy with Source (Recommended)
```bash
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
  --set-env-vars GOOGLE_APPLICATION_CREDENTIALS=service-account-key.json
```

### Option 2: Deploy with Docker
```bash
# Build and submit to Cloud Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/receipt-scanner-api

# Deploy the container
gcloud run deploy receipt-scanner-api \
  --image gcr.io/YOUR_PROJECT_ID/receipt-scanner-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

## Step 5: Configure Service Account

The service account key needs to be available in the container:

### Option A: Use the uploaded service-account-key.json
```bash
# The file is already in your repo, so it will be included in the deployment
# Make sure the GOOGLE_APPLICATION_CREDENTIALS env var points to it
```

### Option B: Use Cloud Run's built-in service account (Recommended)
```bash
# Grant your Cloud Run service the Vision API role
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/vision.imageAnnotator"
```

## Step 6: Test Your Deployed API

After deployment, you'll get a URL like: `https://receipt-scanner-api-xxxxx-uc.a.run.app`

### Test Health Endpoint:
```bash
curl https://YOUR_CLOUD_RUN_URL/api/health
```

### Test Receipt Scanning:
```bash
curl -X POST \
  https://YOUR_CLOUD_RUN_URL/api/scan \
  -F "receipt_image=@receipts/receipt1.jpg"
```

## Cost Estimation

### Free Tier (Monthly):
- 2 million requests
- 400,000 GB-seconds of compute time
- 1 GB network egress

### After Free Tier:
- $0.40 per million requests
- $0.00002400 per GB-second
- $0.12 per GB network egress

**For typical usage**: Usually stays within free tier!

## Monitoring and Management

### View Logs:
```bash
gcloud run services logs tail receipt-scanner-api --region us-central1
```

### Update Service:
```bash
gcloud run services update receipt-scanner-api \
  --region us-central1 \
  --set-env-vars NEW_VAR=value
```

### Delete Service:
```bash
gcloud run services delete receipt-scanner-api --region us-central1
```

## Security Best Practices

1. **Don't commit service account keys** to public repos
2. **Use Cloud Run's built-in service accounts** when possible
3. **Enable authentication** if needed:
   ```bash
   gcloud run services remove-iam-policy-binding receipt-scanner-api \
     --member="allUsers" \
     --role="roles/run.invoker" \
     --region us-central1
   ```

## Troubleshooting

### Common Issues:
1. **Build fails**: Check Dockerfile and requirements.txt
2. **Service account errors**: Verify Vision API is enabled
3. **Memory errors**: Increase memory allocation
4. **Cold start timeouts**: Increase timeout or use min-instances

### Useful Commands:
```bash
# Check service status
gcloud run services describe receipt-scanner-api --region us-central1

# View recent deployments
gcloud run revisions list --service receipt-scanner-api --region us-central1
```

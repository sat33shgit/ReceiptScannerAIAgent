# Render Deployment (100% Free)

## Deploy to Render (Completely Free Option)

### Option 1: One-Click Deploy Button

Add this to your GitHub README for one-click deployment:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/sat33shgit/ReceiptScannerAIAgent)

### Option 2: Manual Deployment

1. **Visit Render**: Go to [render.com](https://render.com)

2. **Sign Up**: Use your GitHub account

3. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Choose `ReceiptScannerAIAgent`

4. **Configure Service**:
   - **Name**: `receipt-scanner-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Instance Type**: `Free`

5. **Environment Variables**:
   - Add `GOOGLE_APPLICATION_CREDENTIALS` = `service-account-key.json`
   - Upload service account file

6. **Deploy**: Click "Create Web Service"

### Features of Render Free Tier:
- ✅ **Always Free**: No time limits
- ✅ **750 hours/month**: Enough for always-on
- ✅ **Automatic HTTPS**: SSL certificates included  
- ✅ **Custom domains**: Free subdomains
- ⚠️ **Cold starts**: 30-second delay after 15min inactivity

### Your API URL:
`https://receipt-scanner-api.onrender.com`

### Test Commands:
```bash
# Health check
curl https://receipt-scanner-api.onrender.com/api/health

# Upload receipt
curl -X POST \
  https://receipt-scanner-api.onrender.com/api/scan \
  -F "receipt_image=@receipt.jpg"
```

## Cost Comparison Summary:

| Platform | Monthly Cost | Cold Starts | Always-On | Difficulty |
|----------|--------------|-------------|-----------|------------|
| **Render** | $0 (Free) | Yes (30s) | No | Easy |
| **Railway** | $0-5 | No | Yes | Easy |
| **Google Cloud Run** | $0-2 | Minimal | No | Medium |
| **Heroku** | $7+ | No | Yes | Easy |

**Recommendation**: Start with **Render** (free), upgrade to **Railway** if you need always-on performance.

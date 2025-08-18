# Railway Deployment Guide

## 🚀 Quick Railway Deployment

### Step 1: Deploy to Railway
1. **Visit**: [railway.app](https://railway.app)
2. **Login**: Use your GitHub account
3. **New Project**: Click "New Project" → "Deploy from GitHub repo"
4. **Select Repository**: Choose `sat33shgit/ReceiptScannerAIAgent`
5. **Deploy**: Click "Deploy Now"

### Step 2: Configure Environment Variables
In your Railway project dashboard:

1. **Go to "Variables" tab**
2. **Add these variables**:

```
PORT=8080
GOOGLE_CLOUD_KEY_JSON={"type":"service_account","project_id":"your-project",...}
```

**For GOOGLE_CLOUD_KEY_JSON**:
- Open your `service-account-key.json` file
- Copy the ENTIRE JSON content (all the text inside the file)
- Paste it as the value for `GOOGLE_CLOUD_KEY_JSON`

### Step 3: Test Your API
After deployment (2-5 minutes), you'll get a URL like:
`https://receiptscanneraiagent-production.up.railway.app`

**Test endpoints**:
```bash
# Health check
curl https://your-app.railway.app/api/health

# Upload receipt
curl -X POST https://your-app.railway.app/api/scan \
  -F "receipt_image=@receipt.jpg"
```

### Step 4: Monitor Your App
- **Logs**: View real-time logs in Railway dashboard
- **Metrics**: See CPU, memory usage
- **Deployments**: Track deployment history

## 💰 Railway Pricing
- **$5 free credit** per month
- **$0.000463 per GB-second** after free credit
- **No cold starts** - always fast!

## 🔄 Auto-Deployments
Railway automatically redeploys when you:
- Push code to your GitHub repository
- Update environment variables
- Change configuration

## 🛠️ Troubleshooting

### Common Issues:
1. **Build fails**: Check `requirements.txt` for missing dependencies
2. **API errors**: Verify `GOOGLE_CLOUD_KEY_JSON` is set correctly
3. **Timeout**: Increase timeout in Railway settings

### Useful Commands:
```bash
# Test locally before deploying
python app.py

# Check if your JSON is valid
python -c "import json; print(json.loads(open('service-account-key.json').read()))"
```

## 🎯 Next Steps
1. **Deploy to Railway** (5 minutes)
2. **Test your API** with sample receipts
3. **Update your mobile app** to use the new API URL
4. **Monitor usage** in Railway dashboard

Your Receipt Scanner API will be live at:
`https://your-app-name.railway.app`

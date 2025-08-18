# Render Deployment - Step by Step

## 🚀 Deploy to Render (Free & Reliable)

### Step 1: Access Render
1. **Go to**: [render.com](https://render.com)
2. **Sign up/Login**: Use your GitHub account

### Step 2: Create Web Service
1. **Click "New +"** → **"Web Service"**
2. **Connect GitHub**: Choose `sat33shgit/ReceiptScannerAIAgent`
3. **Configure Service**:
   - **Name**: `receipt-scanner-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app_simple:app`
   - **Instance Type**: `Free`

### Step 3: Environment Variables
Add in Render dashboard:
```
PORT=10000
GOOGLE_CLOUD_KEY_JSON={"type":"service_account","project_id":"281601491527",...}
```

### Step 4: Deploy
- Click "Create Web Service"
- Render builds and deploys automatically
- More reliable than Railway for Python apps

### Step 5: Test
Your API will be at: `https://receipt-scanner-api.onrender.com`

Test: `https://receipt-scanner-api.onrender.com/api/health`

## ✅ Why Render Works Better:
- Better Python support
- Clearer error messages
- More forgiving with dependencies
- 100% free tier
- Easier debugging

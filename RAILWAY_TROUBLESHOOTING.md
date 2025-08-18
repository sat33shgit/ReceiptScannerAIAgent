# Railway Deployment Troubleshooting

## 🔧 Build Failed? Here's How to Fix It

### Step 1: Push Updated Code
The issue was likely caused by:
- ❌ opencv-python dependency (not needed for Railway)
- ❌ Missing version specifications
- ❌ Streamlit dependency (not needed for API)

**Fixed files:**
- ✅ Updated `requirements.txt` with specific versions
- ✅ Removed unnecessary imports from `app.py`
- ✅ Added `runtime.txt` for Python version
- ✅ Updated `railway.json` configuration

### Step 2: Push to GitHub
```bash
git add .
git commit -m "Fix Railway deployment - remove opencv, add versions"
git push origin main
```

### Step 3: Redeploy on Railway
1. **Go to your Railway project**
2. **Click "Deployments" tab**
3. **Click "Redeploy"** or it will auto-deploy from GitHub

### Step 4: Set Environment Variables
In Railway dashboard → Variables tab:

```
PORT=8080
GOOGLE_CLOUD_KEY_JSON={"type":"service_account","project_id":"281601491527",...}
```

**For GOOGLE_CLOUD_KEY_JSON:**
- Open your `service-account-key.json` file
- Copy ALL the JSON content (entire file)
- Paste it as the variable value

### Step 5: Monitor Build Logs
Watch the build process in Railway:
- ✅ Initialization should complete
- ✅ Build should install packages successfully
- ✅ Deploy should start your Flask app

## 🚨 Common Railway Issues & Fixes

### Issue 1: Build Timeout
**Solution:** Remove heavy packages like opencv-python, tensorflow

### Issue 2: Import Errors
**Solution:** Add specific versions to requirements.txt

### Issue 3: Port Issues
**Solution:** Make sure your app uses `os.environ.get('PORT', 8080)`

### Issue 4: Google Cloud Auth
**Solution:** Use GOOGLE_CLOUD_KEY_JSON environment variable

## ✅ Verification Steps

After successful deployment:

```bash
# Test health endpoint
curl https://your-app.railway.app/api/health

# Should return:
{"status":"healthy","service":"Receipt Scanner AI Agent","version":"1.0.0"}
```

## 🔄 Alternative: Quick Deploy to Render

If Railway keeps failing, try Render (100% free):

1. **Go to:** render.com
2. **Connect GitHub repo**
3. **Use these settings:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - Environment: Python 3
   - Plan: Free

## 📞 Need Help?

If still having issues:
1. Check Railway build logs for specific error
2. Verify all environment variables are set
3. Test locally: `python app.py`
4. Consider using Render as backup option

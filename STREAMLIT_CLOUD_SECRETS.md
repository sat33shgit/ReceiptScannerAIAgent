# Streamlit Cloud Secrets Configuration

## 🚨 **URGENT: Fix for Streamlit Cloud Deployment**

The Streamlit app is failing because the Google Cloud Vision API credentials are not properly configured in Streamlit Cloud secrets.

## 📋 **Step-by-Step Fix:**

### 1. Go to Streamlit Cloud
- Visit: https://share.streamlit.io/
- Find your Receipt Scanner app
- Click the settings (gear) icon

### 2. Navigate to Secrets
- Click "Secrets" in the left sidebar
- You'll see a text editor for secrets configuration

### 3. Copy & Paste This Configuration:

```toml
[gcp_service_account]
type = "service_account"
project_id ="ocrproject-469323"
private_key_id = "26753f2b546698aacbcee7fdd16c455de84e16c8"
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDTWBnXgY9ftH/w\nLBvEvDtOuV+ZRhfpgQdvSJuUoXY7HWTprDktenmxni3tv8g4w9/LgYK2JGE877fZ\ncFrWxD8V5x6WOkmYtnFD/2icbd7SN8dJ45INf0KT9Cja9zQb2VuLk5Wk91N6C4vd\nDCXax2pQgqmMyN6RRP2JtFja6l8tR4iIx1wRGy0x0SfXm98Umtwj/FVXxYqIv9A1\nF/SHgjy7+LMk7ev1KHGLkifb9P+BSC8C9uZ0XP4Bl5k3nojKNADiAWl7jr6QqP6t\ngVX5cUAxt1xUO6SJXGPrzbYNQo2BiaYQZeRrkhxRAGSjsrUfYSR2h7keR0B976oX\nnGVscpJzAgMBAAECggEAANmwlnO/4YbRd4jlhJAy8S0HJbRftXJz6RYSxi5Yar8w\nICk7yJ06R0/8EjqCuDnYlIFZTPrWQTobgIbfp9ZG7INgAHCw+rAC8y41o5Fk77dD\nZ6euD7yOLgvinVcekz7G85bv4YMo9Tquncmqs4P1pwBG0xS8rgpVqlf2KM0L/hWd\ns8PAtb+nT/0MLuF75kYEq+eYTeXVm1QY7IC0lmxu785Hy8zoscxSSObOdI9a7SG2\nA+x+5+1mJmLFWKIcVvKPTAKLJxtYWkhtYjMpofukBTy4TqYF84ovua2e0HueAXwd\nVAO8PQzY+QW2ko/kCKiJTiRyaQQ19nGcRp6UfKsHTQKBgQDpZwAZmSnA18Nbk0i/\n0NOBdo4FGGA07NXSLvlORuuXobgih2vJakIY4kFth3Dfqz6TnnR6zLSv/luLxf5l\nopVXLDb5+A7Sse6zo6C7dNyZYneYwZDAQfNaxQ637SuKCimd8qiz9WbfblmBD3M1\nlotRNQ3WgpAKDWXvlSy4m0g8nwKBgQDnzmBgMXV3hGXihuVUnmaIOEGFgw7PYhcB\nt7QMFn+kbmNwbgnw8cr3he4SnvIkfrbIDxCyk9Q9q8wuYi4jAXwrRacBBB1CVcDJ\n4vPttOFMSzCsQwnp25s3MH0ZQTX/sSN3eZsyDoeVZ2gP/lASMtM5tqIN8D7rMEDR\neIVkdP2FrQKBgQCDxlRnH3NUXjz80d3r9jHD0TSDqex/VQuvnDfDOwU+Wd7FF+IC\nGIzy0aMQ/Lv8fAlbfMXUowiMqLX05zcnGLDqQ5tSa/uqdy0GnSZdT7BQpShSxU49\nTb7gi4swyqWfTPeMJnmbCL0o/ntoA1oPckx779E9P/+kvUXFC1rxazJQjwKBgQDm\nw0KaQGJqOrmayyOeG5qC3U4M9a1WspWothJdPkCPlv0TPdhTrsGZrBCXJPh1cFfR\nzX2X6SaOxmobes3nN2E/SrW4gzoFgYzM7kxbRYhMBUZNFufVkTNxu6mt7IcvJk7i\nb4MaT/CVwT2NPmTD2SkB+VhWe+aHB6BfZ5WTrgt8eQKBgEmVOXYgBJWWD1l3WsMQ\nj0Q0oJZMEBnZuAU/FnqmQhAY8Fk75JXYwof4h2wwtOuaYeCN3GIe/Lp0iZkJp61h\neWAqwYfm86Tczc7jGMg00WSGn9GNafowgt6dvpSR+nTjqlnz1XA+iYFfQ4dye5MT\n+PtTvPfcyYyPJ8nLghIIauYG\n-----END PRIVATE KEY-----\n"
client_email = "vision-ocr-service@ocrproject-469323.iam.gserviceaccount.com"
client_id = "118233477061498173889"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/vision-ocr-service%40ocrproject-469323.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

### 4. Save and Restart
- Click "Save" 
- The app will automatically restart
- The error should be resolved

## ✅ **Expected Result:**
After adding these secrets, the Streamlit app should:
- Successfully authenticate with Google Cloud Vision API
- Process receipt images without errors
- Extract store names, amounts, and dates correctly

## 🔐 **Security Note:**
These credentials are already exposed in your local repository. For production applications, you should:
1. Regenerate service account keys
2. Use proper secret management
3. Restrict API key permissions to minimum required scope

## 📞 **Need Help?**
If you're still having issues:
1. Double-check that all fields are copied exactly
2. Ensure there are no extra spaces or characters
3. Verify the Google Cloud Vision API is enabled in your project
4. Check that the service account has proper permissions

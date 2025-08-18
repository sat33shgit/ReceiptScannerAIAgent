# Keep API Warm - Cron Job Setup
# This prevents cold starts by pinging your API every 10 minutes

# Option 1: Use GitHub Actions (Free)
# Create .github/workflows/keep-warm.yml:

name: Keep API Warm
on:
  schedule:
    - cron: '*/10 * * * *'  # Every 10 minutes

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping API
        run: |
          curl -f https://your-api-url.onrender.com/api/health || true

# Option 2: Use UptimeRobot (Free)
# 1. Go to uptimerobot.com
# 2. Add your API URL: https://your-api-url.onrender.com/api/health
# 3. Set check interval: 5 minutes
# 4. UptimeRobot will ping your API and keep it warm

# Option 3: Use Cron-Job.org (Free)
# 1. Go to cron-job.org
# 2. Create job to call: https://your-api-url.onrender.com/api/health
# 3. Set frequency: Every 10 minutes

# Your API will stay warm and respond in ~500ms instead of 30 seconds!

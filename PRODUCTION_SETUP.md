# 🚀 GoPay Production Setup Guide

**Congratulations!** Your IntaSend account is verified. Follow this guide to deploy GoPay to production.

---

## 📋 Prerequisites

- ✅ IntaSend account verified
- ✅ Supabase project created
- ✅ Database migration completed (sandbox)
- ✅ Local testing completed
- [ ] Production server/hosting ready
- [ ] Domain with HTTPS configured

---

## Step 1: Get Production API Keys

### IntaSend Dashboard

1. **Login to Production Dashboard**
   - Go to https://dashboard.intasend.com
   - Make sure you're in **PRODUCTION** mode (check top-right corner)

2. **Navigate to API Keys**
   - Click **Settings** → **API Keys**
   - You should see two sections: Sandbox and Production

3. **Copy Production Keys**
   - **Secret Key**: Starts with `ISSecretKey_live_...`
   - **Publishable Key**: Starts with `ISPubKey_live_...`
   - ⚠️ **NEVER** share your secret key or commit it to git

4. **Save Keys Securely**
   - Store in password manager
   - You'll add these to `.env` file later

---

## Step 2: Enable Production Services

### Enable M-Pesa Collections

1. Go to **Collections** → **M-Pesa**
2. Ensure **M-Pesa STK Push** is enabled
3. Check that status shows **Active** (not Pending)

### Enable M-Pesa Payouts

1. Go to **Payouts** → **M-Pesa**
2. Enable **M-Pesa Disbursements**
3. Set approval mode: **No approval required** (for automatic payouts)
4. Complete any required verification steps

### Verify Business Information

1. Go to **Settings** → **Business Profile**
2. Ensure all information is complete and accurate
3. Verify contact details are correct

---

## Step 3: Configure Production Environment

### Create Production .env File

```bash
# Copy production template
cp env.production.example .env.production

# Edit with your production values
nano .env.production  # or use your preferred editor
```

### Required Configuration

Update these values in `.env.production`:

```env
# Your production domain
BASE_PUBLIC_URL=https://gopay.yourdomain.com

# Supabase credentials
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key

# IntaSend PRODUCTION keys
INTASEND_API_KEY=ISSecretKey_live_xxxxx
INTASEND_PUBLISHABLE_KEY=ISPubKey_live_xxxxx
INTASEND_TEST_MODE=false  # IMPORTANT: false for production!

# Platform fees (adjust as needed)
PLATFORM_FEE_PERCENTAGE=0.5
PLATFORM_FEE_FIXED=0
```

---

## Step 4: Test Production API Connection

Before deploying, test that your production keys work:

### Create Test Script

```python
# test_production_api.py
import os
from dotenv import load_dotenv
import requests

# Load production environment
load_dotenv('.env.production')

api_key = os.getenv('INTASEND_API_KEY')
base_url = "https://payment.intasend.com/api/v1"  # Production URL

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Test wallet balance
response = requests.get(f"{base_url}/wallets/", headers=headers)

if response.status_code == 200:
    print("✅ API Connection Successful!")
    print(f"Wallet Balance: {response.json()}")
else:
    print("❌ API Connection Failed!")
    print(f"Status: {response.status_code}")
    print(f"Error: {response.text}")
```

### Run Test

```bash
python test_production_api.py
```

Expected output:
```
✅ API Connection Successful!
Wallet Balance: {'currency': 'KES', 'available_balance': '0.00', ...}
```

---

## Step 5: Fund Production Wallet

⚠️ **IMPORTANT**: You need funds in your IntaSend wallet to process payouts!

### Add Funds

1. Go to IntaSend Dashboard → **Wallet**
2. Click **Add Funds**
3. Choose funding method:
   - **M-Pesa**: Instant transfer
   - **Bank Transfer**: Takes 1-2 business days
   - **Card**: Instant (may have fees)

4. **Recommended Starting Amount**: 10,000 - 50,000 KES
   - This depends on your expected transaction volume
   - You can add more funds anytime

### Monitor Wallet Balance

- Set up low balance alerts in IntaSend dashboard
- Check balance regularly: Dashboard → Wallet
- Add funds before it runs out to avoid failed payouts

---

## Step 6: Run Database Migration

If you haven't already run the migration on production database:

### In Supabase Dashboard

1. Go to your Supabase project
2. Navigate to **SQL Editor**
3. Click **New Query**
4. Copy contents of `database/intasend_migration.sql`
5. Click **Run**

### Verify Migration

```sql
-- Check new tables created
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('payouts', 'platform_fees');

-- Should return 2 rows

-- Check new columns added
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'transactions' 
AND column_name LIKE '%intasend%';

-- Should return 6 columns
```

---

## Step 7: Deploy to Production

### Option A: Deploy to Railway

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Initialize Project**
   ```bash
   railway init
   railway link
   ```

3. **Add Environment Variables**
   ```bash
   # Add all variables from .env.production
   railway variables set INTASEND_API_KEY="your-key-here"
   railway variables set INTASEND_PUBLISHABLE_KEY="your-pub-key"
   railway variables set INTASEND_TEST_MODE="false"
   # ... add all other variables
   ```

4. **Deploy**
   ```bash
   railway up
   ```

5. **Get Domain**
   ```bash
   railway domain
   # Or add custom domain in Railway dashboard
   ```

### Option B: Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   heroku login
   ```

2. **Create App**
   ```bash
   heroku create gopay-your-name
   ```

3. **Add Buildpack**
   ```bash
   heroku buildpacks:set heroku/python
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set INTASEND_API_KEY="your-key-here"
   heroku config:set INTASEND_PUBLISHABLE_KEY="your-pub-key"
   heroku config:set INTASEND_TEST_MODE="false"
   # ... add all other variables
   ```

5. **Deploy**
   ```bash
   git push heroku master
   ```

6. **Open App**
   ```bash
   heroku open
   ```

### Option C: Deploy to VPS (Ubuntu)

```bash
# SSH into your server
ssh user@your-server-ip

# Clone repository
git clone https://github.com/DaudiKi/GoPay.git
cd GoPay

# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Copy production environment
cp env.production.example .env
# Edit .env with your production values

# Install and configure systemd service
sudo nano /etc/systemd/system/gopay.service
```

**gopay.service** file:
```ini
[Unit]
Description=GoPay FastAPI Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/GoPay
Environment="PATH=/home/ubuntu/GoPay/venv/bin"
ExecStart=/home/ubuntu/GoPay/venv/bin/uvicorn app.main_intasend:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl start gopay
sudo systemctl enable gopay

# Configure Nginx as reverse proxy
sudo nano /etc/nginx/sites-available/gopay
```

**Nginx configuration**:
```nginx
server {
    listen 80;
    server_name gopay.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/gopay /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d gopay.yourdomain.com
```

---

## Step 8: Configure Webhooks

### Create Webhook in IntaSend

1. **Go to Webhook Settings**
   - Dashboard → **Settings** → **Webhooks**
   - Click **Add Webhook**

2. **Configure Webhook**
   ```
   URL: https://gopay.yourdomain.com/api/webhooks/intasend
   ```

3. **Select Events**
   - ✅ `payment.collection.completed`
   - ✅ `payment.collection.failed`
   - ✅ `payout.completed`
   - ✅ `payout.failed`

4. **Save and Get Secret**
   - Click **Create**
   - Copy the **Webhook Secret** (starts with `whs_`)
   - Add to production environment variables:
     ```bash
     # Railway/Heroku
     railway variables set INTASEND_WEBHOOK_SECRET="whs_xxxxx"
     # or
     heroku config:set INTASEND_WEBHOOK_SECRET="whs_xxxxx"
     ```

### Test Webhook

1. **Test from IntaSend Dashboard**
   - Go to Webhooks → Your webhook
   - Click **Test**
   - Check if test event received

2. **Check Application Logs**
   ```bash
   # Railway
   railway logs
   
   # Heroku
   heroku logs --tail
   
   # VPS
   sudo journalctl -u gopay -f
   ```

3. **Look for Log Entry**
   ```
   INFO: Webhook received: COMPLETE - test_xxxxx
   INFO: Payment collected. Payout scheduled...
   ```

---

## Step 9: End-to-End Production Test

### Register Test Driver

```bash
curl -X POST https://gopay.yourdomain.com/api/register_driver \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Driver Production",
    "phone": "254YOUR_REAL_NUMBER",
    "email": "your-email@example.com",
    "vehicle_type": "boda",
    "vehicle_number": "TEST 001P"
  }'
```

Save the `driver_id` and `qr_code_url` from response.

### Test Payment Flow

1. **Open payment page on mobile browser**
   ```
   https://gopay.yourdomain.com/pay?driver_id=YOUR_ID&phone=254YOUR_NUMBER
   ```

2. **Make small test payment**
   - Enter amount: **10 KES** (small amount for testing)
   - Verify phone number is correct
   - Click **Pay Now**

3. **Complete M-Pesa prompt**
   - You should receive STK push on your phone
   - Enter your M-Pesa PIN
   - Confirm payment

4. **Verify payment collected**
   - Check your M-Pesa SMS - should show 10 KES paid
   - Check IntaSend Dashboard → Collections
   - Should show successful collection

5. **Verify payout received**
   - Within 1-2 minutes, driver should receive payout
   - Check M-Pesa SMS - should show ~9.95 KES received (10 - 0.5% fee)
   - Check IntaSend Dashboard → Payouts
   - Should show successful payout

6. **Check Application**
   - Visit: `https://gopay.yourdomain.com/driver/YOUR_DRIVER_ID/dashboard`
   - Should show transaction and payout
   - Visit: `https://gopay.yourdomain.com/admin/dashboard`
   - Should show statistics

### Verify in Database

```sql
-- Check transaction
SELECT * FROM transactions ORDER BY created_at DESC LIMIT 1;

-- Check payout
SELECT * FROM payouts ORDER BY created_at DESC LIMIT 1;

-- Check platform fee
SELECT * FROM platform_fees ORDER BY created_at DESC LIMIT 1;
```

---

## Step 10: Monitoring Setup

### Application Monitoring

1. **Setup Error Tracking** (Optional but Recommended)
   ```bash
   # Install Sentry
   pip install sentry-sdk[fastapi]
   ```
   
   Add to `app/main_intasend.py`:
   ```python
   import sentry_sdk
   
   if os.getenv('SENTRY_DSN'):
       sentry_sdk.init(dsn=os.getenv('SENTRY_DSN'))
   ```

2. **Setup Uptime Monitoring**
   - Use services like UptimeRobot, Pingdom, or StatusCake
   - Monitor: `https://gopay.yourdomain.com/health`
   - Alert if down for > 5 minutes

3. **Setup Log Aggregation**
   - Use Papertrail, Loggly, or similar
   - Monitor for:
     - "Payment failed"
     - "Payout failed"
     - "Webhook"
     - "ERROR"

### Business Monitoring

1. **Daily Checks**
   - Check wallet balance
   - Review failed transactions
   - Monitor payout success rate

2. **Weekly Reports**
   ```sql
   -- Weekly revenue report
   SELECT 
       DATE_TRUNC('week', created_at) as week,
       COUNT(*) as transactions,
       SUM(amount_paid) as total_revenue,
       SUM(platform_fee) as platform_fees,
       SUM(driver_amount) as driver_payouts
   FROM transactions
   WHERE collection_status = 'completed'
   GROUP BY week
   ORDER BY week DESC;
   ```

---

## 🎯 Go-Live Checklist

Before announcing to drivers:

- [ ] Production API keys configured
- [ ] Webhook configured and tested
- [ ] Wallet funded (sufficient for expected volume)
- [ ] Database migration completed
- [ ] End-to-end payment tested with real money
- [ ] Payout received by test driver
- [ ] SSL/HTTPS working on domain
- [ ] Monitoring and alerting setup
- [ ] Error tracking configured
- [ ] Backup strategy in place
- [ ] Support procedures documented
- [ ] Team trained on new system

---

## 🚨 Troubleshooting

### Payment Collection Failed

**Check:**
1. API keys are production keys (start with `ISSecretKey_live_`)
2. `INTASEND_TEST_MODE=false` in environment
3. Phone number format: `254XXXXXXXXX`
4. IntaSend collections service is active

**Logs to check:**
```
ERROR: Collection initiation failed: ...
```

### Payout Failed

**Check:**
1. Wallet has sufficient balance
2. Payout service is enabled in IntaSend
3. Driver phone number is correct
4. "No approval required" is set for payouts

**Logs to check:**
```
ERROR: Payout initiation failed: ...
```

### Webhook Not Received

**Check:**
1. Webhook URL is publicly accessible (not localhost)
2. HTTPS is configured
3. Webhook secret matches environment variable
4. Firewall allows incoming connections

**Test webhook:**
```bash
curl -X POST https://gopay.yourdomain.com/api/webhooks/intasend \
  -H "Content-Type: application/json" \
  -d '{"state": "COMPLETE", "api_ref": "test"}'
```

---

## 📞 Support

### IntaSend Support
- **Email**: support@intasend.com
- **Phone**: +254 (check dashboard for latest)
- **Docs**: https://developers.intasend.com
- **Dashboard**: https://dashboard.intasend.com

### GoPay Issues
- Check logs first
- Review this documentation
- Test in sandbox mode if needed
- Contact your development team

---

## 🎉 You're Live!

Once everything is working:

1. **Announce to drivers**
2. **Monitor closely for first 24 hours**
3. **Be ready for support questions**
4. **Gather feedback**
5. **Optimize based on usage**

**Good luck! 🚀**


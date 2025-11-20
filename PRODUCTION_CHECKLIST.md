# ✅ GoPay Production Deployment Checklist

**Your IntaSend account is verified!** Use this checklist to deploy to production.

---

## 📋 Pre-Deployment

### IntaSend Account
- [x] Account created and verified ✅
- [ ] Production API keys obtained
- [ ] Collections (M-Pesa STK) enabled
- [ ] Payouts (M-Pesa Disbursements) enabled
- [ ] Payout approval set to "No approval required"

### Supabase Database
- [ ] Supabase project created
- [ ] Database migration executed (`intasend_migration.sql`)
- [ ] Migration verified (run `python verify_database.py`)
- [ ] Database backup created

### Local Environment
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Sandbox testing completed
- [ ] Production .env file created
- [ ] Production API connection tested (`python test_production_api.py`)

---

## 🔑 Step 1: Get Production Credentials

### IntaSend Production Keys

1. Login to: https://dashboard.intasend.com
2. Switch to **PRODUCTION** mode (top-right toggle)
3. Navigate to: **Settings** → **API Keys**
4. Copy and save securely:
   - [ ] Secret Key (starts with `ISSecretKey_live_`)
   - [ ] Publishable Key (starts with `ISPubKey_live_`)

### Supabase Credentials

1. Login to: https://app.supabase.com
2. Select your project
3. Go to: **Settings** → **API**
4. Copy:
   - [ ] Project URL
   - [ ] Anon/Public Key

---

## 🗄️ Step 2: Database Setup

### Run Migration

1. Open Supabase: https://app.supabase.com
2. Go to: **SQL Editor**
3. Create new query
4. Copy contents from: `database/intasend_migration.sql`
5. Execute query
6. Verify success:
   - [ ] No errors in execution
   - [ ] New tables created: `payouts`, `platform_fees`
   - [ ] Transactions table updated with IntaSend columns

### Verify Migration

```bash
python verify_database.py
```

Expected: **✅ Database Verification Passed!**

---

## ⚙️ Step 3: Configure Production Environment

### Create Production Config

```bash
cp env.production.example .env.production
```

### Edit Configuration

Open `.env.production` and update:

```env
# Your production domain
BASE_PUBLIC_URL=https://gopay.yourdomain.com

# Supabase (from Step 1)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here

# IntaSend PRODUCTION keys (from Step 1)
INTASEND_API_KEY=ISSecretKey_live_xxxxx
INTASEND_PUBLISHABLE_KEY=ISPubKey_live_xxxxx
INTASEND_TEST_MODE=false  # ⚠️ MUST be false for production!

# Platform fees (adjust as needed)
PLATFORM_FEE_PERCENTAGE=0.5
PLATFORM_FEE_FIXED=0
```

**Checklist:**
- [ ] `BASE_PUBLIC_URL` set to your domain
- [ ] Supabase credentials correct
- [ ] IntaSend keys are PRODUCTION keys (start with `_live_`)
- [ ] `INTASEND_TEST_MODE=false`
- [ ] Platform fee configured

---

## 🧪 Step 4: Test Locally

### Test API Connection

```bash
python test_production_api.py
```

**Expected output:**
```
✅ API Connection Successful!
💰 Wallet Balance: X.XX KES
✅ All Tests Passed!
```

**Checklist:**
- [ ] API connection successful
- [ ] Wallet accessible
- [ ] Collections service accessible
- [ ] Payouts service accessible
- [ ] No authentication errors

---

## 🚀 Step 5: Deploy to Hosting

Choose your hosting platform:

### Option A: Railway ⭐ Recommended

```bash
# Install CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Get domain
railway domain
```

**Set all environment variables:**
```bash
railway variables set INTASEND_API_KEY="ISSecretKey_live_xxxxx"
railway variables set INTASEND_PUBLISHABLE_KEY="ISPubKey_live_xxxxx"
railway variables set INTASEND_TEST_MODE="false"
railway variables set SUPABASE_URL="your-supabase-url"
railway variables set SUPABASE_ANON_KEY="your-supabase-key"
railway variables set PLATFORM_FEE_PERCENTAGE="0.5"
railway variables set PLATFORM_FEE_FIXED="0"
railway variables set BASE_PUBLIC_URL="your-railway-domain"
```

**Checklist:**
- [ ] Railway CLI installed
- [ ] Project deployed
- [ ] All environment variables set
- [ ] Application accessible via HTTPS
- [ ] Health check passes: `/health`

### Option B: Heroku

```bash
# Create app
heroku create gopay-production

# Set variables
heroku config:set \
  INTASEND_API_KEY="ISSecretKey_live_xxxxx" \
  INTASEND_PUBLISHABLE_KEY="ISPubKey_live_xxxxx" \
  INTASEND_TEST_MODE="false" \
  SUPABASE_URL="your-supabase-url" \
  SUPABASE_ANON_KEY="your-supabase-key" \
  PLATFORM_FEE_PERCENTAGE="0.5" \
  BASE_PUBLIC_URL="your-heroku-domain"

# Deploy
git push heroku master
```

**Checklist:**
- [ ] Heroku app created
- [ ] All environment variables set
- [ ] Application deployed
- [ ] Application accessible via HTTPS
- [ ] Health check passes

---

## 🪝 Step 6: Configure Webhook

### IntaSend Dashboard

1. Go to: https://dashboard.intasend.com/settings/webhooks
2. Click: **Add Webhook**
3. Configure:
   ```
   URL: https://your-deployed-domain.com/api/webhooks/intasend
   ```
4. Enable events:
   - [x] `payment.collection.completed`
   - [x] `payment.collection.failed`
   - [x] `payout.completed`
   - [x] `payout.failed`
5. Save webhook
6. Copy webhook secret (starts with `whs_`)

### Add Webhook Secret to Environment

```bash
# Railway
railway variables set INTASEND_WEBHOOK_SECRET="whs_xxxxx"

# Heroku
heroku config:set INTASEND_WEBHOOK_SECRET="whs_xxxxx"
```

### Test Webhook

1. In IntaSend dashboard, find your webhook
2. Click **Test** button
3. Check application logs:
   ```bash
   # Railway
   railway logs
   
   # Heroku
   heroku logs --tail
   ```
4. Look for: `INFO: Webhook received: ...`

**Checklist:**
- [ ] Webhook created in IntaSend
- [ ] Webhook URL correct
- [ ] All events enabled
- [ ] Webhook secret added to environment
- [ ] Test webhook successful
- [ ] Webhook received in logs

---

## 💰 Step 7: Fund Production Wallet

### Add Funds to IntaSend Wallet

1. Go to: https://dashboard.intasend.com/wallet
2. Click: **Add Funds**
3. Choose: **M-Pesa** (instant)
4. Amount: Start with 10,000 - 50,000 KES
5. Complete M-Pesa payment on phone
6. Verify balance updated

**Checklist:**
- [ ] Funds added to wallet
- [ ] Balance visible in dashboard
- [ ] Sufficient for expected payout volume
- [ ] Low balance alerts configured

---

## 🧪 Step 8: End-to-End Production Test

### Register Test Driver

```bash
curl -X POST https://your-domain.com/api/register_driver \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Driver Production",
    "phone": "254YOUR_REAL_NUMBER",
    "email": "test@example.com",
    "vehicle_type": "boda",
    "vehicle_number": "TEST001"
  }'
```

**Save from response:**
- [ ] `driver_id`
- [ ] `qr_code_url`

### Make Test Payment (Real Money!)

1. Open on mobile: `https://your-domain.com/pay?driver_id=DRIVER_ID&phone=254YOUR_NUMBER`
2. Enter amount: **10 KES** (small test amount)
3. Click **Pay Now**
4. Complete M-Pesa prompt
5. Wait 1-2 minutes

### Verify Payment Flow

**Check M-Pesa SMS:**
- [ ] Payment confirmation received (10 KES paid)
- [ ] Payout received (~9.95 KES after 0.5% fee)

**Check IntaSend Dashboard:**
- [ ] Collection shows as completed
- [ ] Payout shows as completed

**Check Application:**
- [ ] Visit: `https://your-domain.com/driver/DRIVER_ID/dashboard`
- [ ] Transaction shows
- [ ] Payout shows
- [ ] Amounts correct

**Check Database:**
```sql
-- In Supabase SQL Editor
SELECT * FROM transactions ORDER BY created_at DESC LIMIT 1;
SELECT * FROM payouts ORDER BY created_at DESC LIMIT 1;
SELECT * FROM platform_fees ORDER BY created_at DESC LIMIT 1;
```

- [ ] Transaction record created
- [ ] Collection status = 'completed'
- [ ] Payout record created
- [ ] Payout status = 'completed'
- [ ] Platform fee recorded

---

## 🎯 Step 9: Go Live!

### Final Verification

- [ ] All previous steps completed ✅
- [ ] End-to-end test successful ✅
- [ ] Payout received ✅
- [ ] Database records correct ✅
- [ ] Dashboards working ✅
- [ ] Webhooks functioning ✅
- [ ] SSL/HTTPS enabled ✅
- [ ] Monitoring setup ✅

### Register Real Drivers

For each driver:

1. Register via API:
   ```bash
   curl -X POST https://your-domain.com/api/register_driver \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Driver Name",
       "phone": "254XXXXXXXXX",
       "email": "driver@email.com",
       "vehicle_type": "boda",
       "vehicle_number": "KXX XXX"
     }'
   ```

2. Download QR code from `qr_code_url`
3. Print or share QR with driver
4. Driver displays QR for passengers

**Checklist:**
- [ ] First driver registered
- [ ] QR code downloaded and printed
- [ ] Driver instructed on usage
- [ ] Driver tested QR scanning

---

## 📊 Step 10: Monitoring & Maintenance

### Setup Monitoring

**Application Health:**
- [ ] Uptime monitoring configured (UptimeRobot, etc.)
- [ ] Error tracking setup (Sentry, optional)
- [ ] Log monitoring configured

**Monitor endpoint:**
```
https://your-domain.com/health
```

### Daily Checks

- [ ] Check wallet balance
- [ ] Review failed transactions (if any)
- [ ] Check payout success rate
- [ ] Review logs for errors

### Weekly Reports

```sql
-- Run in Supabase SQL Editor
SELECT 
    DATE_TRUNC('week', created_at) as week,
    COUNT(*) as transactions,
    SUM(amount_paid) as total_collected,
    SUM(platform_fee) as platform_revenue,
    SUM(driver_amount) as driver_payouts
FROM transactions
WHERE collection_status = 'completed'
GROUP BY week
ORDER BY week DESC;
```

---

## 🚨 Troubleshooting

### Payment Collection Fails

**Check:**
- [ ] API keys are production keys
- [ ] `INTASEND_TEST_MODE=false`
- [ ] Phone number format: `254XXXXXXXXX`
- [ ] Collections enabled in IntaSend

### Payout Fails

**Check:**
- [ ] Wallet has sufficient balance
- [ ] Payouts enabled in IntaSend
- [ ] "No approval required" is set
- [ ] Driver phone number correct

### Webhook Not Received

**Check:**
- [ ] Webhook URL is correct
- [ ] URL is publicly accessible (HTTPS)
- [ ] Webhook secret matches environment
- [ ] Test webhook from IntaSend dashboard

### Quick Diagnostic

```bash
# Test API
python test_production_api.py

# Check logs
railway logs  # or: heroku logs --tail

# Test webhook manually
curl -X POST https://your-domain.com/api/webhooks/intasend \
  -H "Content-Type: application/json" \
  -d '{"state": "COMPLETE", "api_ref": "test"}'
```

---

## 📞 Support Resources

### Documentation
- [ ] `PRODUCTION_SETUP.md` - Detailed setup guide
- [ ] `QUICK_PRODUCTION_DEPLOY.md` - Fast deployment guide
- [ ] `INTASEND_IMPLEMENTATION.md` - Technical details

### IntaSend Support
- Email: support@intasend.com
- Dashboard: https://dashboard.intasend.com
- Docs: https://developers.intasend.com

### Application
- API Docs: `https://your-domain.com/docs`
- Admin Dashboard: `https://your-domain.com/admin/dashboard`

---

## ✅ Deployment Complete!

**Congratulations! 🎉**

Your GoPay system is now live in production with:
- ✅ Automatic payment collection
- ✅ Instant driver payouts
- ✅ Real-time tracking
- ✅ Production-grade reliability

### Next Steps

1. Monitor first few transactions closely
2. Gather driver feedback
3. Optimize based on usage patterns
4. Scale as your business grows

**Thank you for using GoPay! 🚀**

---

**Deployment Date:** ________________
**Deployed By:** ________________
**Production URL:** ________________
**Status:** ________________


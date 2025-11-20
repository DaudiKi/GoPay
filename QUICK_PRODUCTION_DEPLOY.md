# ⚡ Quick Production Deployment Guide

**Fast track guide** to get GoPay live in production. Your IntaSend account is verified ✅

---

## 🎯 Quick Overview

1. Get production keys (5 min)
2. Configure environment (5 min)
3. Test API locally (2 min)
4. Deploy to hosting (15 min)
5. Setup webhook (5 min)
6. Fund wallet (5 min)
7. Test end-to-end (5 min)

**Total time: ~40 minutes**

---

## Step 1: Get Production Keys (5 min)

1. Login: https://dashboard.intasend.com
2. Switch to **PRODUCTION** mode (top-right)
3. Go to: **Settings** → **API Keys**
4. Copy:
   - **Secret Key**: `ISSecretKey_live_...`
   - **Publishable Key**: `ISPubKey_live_...`

---

## Step 2: Configure Environment (5 min)

```bash
# Create production env file
cp env.production.example .env.production

# Edit with your keys
nano .env.production
```

**Update these:**
```env
# Your domain (or use hosting-provided domain)
BASE_PUBLIC_URL=https://gopay.yourdomain.com

# Your Supabase credentials (from https://app.supabase.com)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-key-here

# IntaSend PRODUCTION keys
INTASEND_API_KEY=ISSecretKey_live_xxxxx
INTASEND_PUBLISHABLE_KEY=ISPubKey_live_xxxxx
INTASEND_TEST_MODE=false  # ⚠️ IMPORTANT: false for production

# Optional: Adjust fees
PLATFORM_FEE_PERCENTAGE=0.5
PLATFORM_FEE_FIXED=0
```

---

## Step 3: Test API Connection (2 min)

```bash
# Run test script
python test_production_api.py
```

**Expected output:**
```
✅ API Connection Successful!
💰 Wallet Balance: 0.00 KES
✅ All Tests Passed!
```

If this works, your keys are correct! ✅

---

## Step 4: Deploy to Hosting (15 min)

### Option A: Railway (Recommended - Easiest)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Set environment variables (do this for ALL variables from .env.production)
railway variables set INTASEND_API_KEY="ISSecretKey_live_xxxxx"
railway variables set INTASEND_PUBLISHABLE_KEY="ISPubKey_live_xxxxx"
railway variables set INTASEND_TEST_MODE="false"
railway variables set SUPABASE_URL="your-supabase-url"
railway variables set SUPABASE_ANON_KEY="your-supabase-key"
railway variables set PLATFORM_FEE_PERCENTAGE="0.5"
railway variables set PLATFORM_FEE_FIXED="0"
railway variables set BASE_PUBLIC_URL="your-railway-url"  # Update after getting domain

# Deploy
railway up

# Get your URL
railway domain
```

Your app is now live! Copy the URL (e.g., `https://gopay-production-xxx.railway.app`)

**Update BASE_PUBLIC_URL:**
```bash
railway variables set BASE_PUBLIC_URL="https://gopay-production-xxx.railway.app"
```

### Option B: Heroku

```bash
# Install Heroku CLI & login
heroku login

# Create app
heroku create gopay-production

# Set variables (shorter syntax)
heroku config:set \
  INTASEND_API_KEY="ISSecretKey_live_xxxxx" \
  INTASEND_PUBLISHABLE_KEY="ISPubKey_live_xxxxx" \
  INTASEND_TEST_MODE="false" \
  SUPABASE_URL="your-supabase-url" \
  SUPABASE_ANON_KEY="your-supabase-key" \
  PLATFORM_FEE_PERCENTAGE="0.5" \
  PLATFORM_FEE_FIXED="0"

# Deploy
git push heroku master

# Get URL
heroku info -s | grep web_url

# Update BASE_PUBLIC_URL
heroku config:set BASE_PUBLIC_URL="your-heroku-url"
```

---

## Step 5: Setup Webhook (5 min)

1. **Go to IntaSend Dashboard**
   - https://dashboard.intasend.com
   - **Settings** → **Webhooks**

2. **Add Webhook**
   ```
   URL: https://your-deployed-url.com/api/webhooks/intasend
   ```

3. **Select Events**
   - ✅ `payment.collection.completed`
   - ✅ `payment.collection.failed`
   - ✅ `payout.completed`
   - ✅ `payout.failed`

4. **Save & Copy Secret**
   - Copy the webhook secret (starts with `whs_`)
   
5. **Add to Environment**
   ```bash
   # Railway
   railway variables set INTASEND_WEBHOOK_SECRET="whs_xxxxx"
   
   # Heroku
   heroku config:set INTASEND_WEBHOOK_SECRET="whs_xxxxx"
   ```

6. **Test Webhook**
   - In IntaSend dashboard, click **Test** next to your webhook
   - Check logs to confirm received:
   ```bash
   # Railway
   railway logs
   
   # Heroku
   heroku logs --tail
   ```

---

## Step 6: Fund Wallet (5 min)

⚠️ **Required for payouts!**

1. **Go to Wallet**
   - Dashboard → **Wallet**

2. **Add Funds**
   - Click **Add Funds**
   - Choose **M-Pesa** (instant)
   - Amount: 10,000 - 50,000 KES (start with what you're comfortable with)
   - Follow M-Pesa prompt on phone

3. **Verify Balance**
   - Should show in dashboard immediately
   - Can also check via:
   ```bash
   python test_production_api.py
   ```

---

## Step 7: Test End-to-End (5 min)

### Register Test Driver

```bash
curl -X POST https://your-deployed-url.com/api/register_driver \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Driver",
    "phone": "254YOUR_REAL_NUMBER",
    "email": "test@example.com",
    "vehicle_type": "boda",
    "vehicle_number": "TEST123"
  }'
```

Save the `driver_id` from response.

### Make Test Payment

1. **Open payment page on phone**
   ```
   https://your-deployed-url.com/pay?driver_id=DRIVER_ID&phone=254YOUR_NUMBER
   ```

2. **Pay small amount**
   - Enter: 10 KES
   - Click **Pay Now**
   - Complete M-Pesa prompt

3. **Verify**
   - Check M-Pesa SMS - payment sent
   - Wait 1-2 minutes
   - Check M-Pesa SMS - payout received (~9.95 KES)

4. **Check Dashboard**
   ```
   https://your-deployed-url.com/driver/DRIVER_ID/dashboard
   ```

If you received the payout, **everything works!** 🎉

---

## ✅ Production Checklist

Before going live with real drivers:

- [ ] API test passed
- [ ] App deployed to hosting
- [ ] Webhook configured and tested
- [ ] Wallet funded
- [ ] End-to-end test with real money succeeded
- [ ] Payout received
- [ ] Dashboard working
- [ ] SSL/HTTPS enabled (automatic with Railway/Heroku)

---

## 🚀 You're Live!

### Next Steps

1. **Register your first real driver**
   ```bash
   curl -X POST https://your-deployed-url.com/api/register_driver \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Driver Name",
       "phone": "254XXXXXXXXX",
       "email": "driver@email.com",
       "vehicle_type": "boda",
       "vehicle_number": "KXX XXX"
     }'
   ```

2. **Download QR code**
   - Get `qr_code_url` from response
   - Download and print
   - Give to driver

3. **Driver can start receiving payments!**
   - Passengers scan QR → Pay → Driver gets money automatically

### Monitor Your Application

**Check logs:**
```bash
# Railway
railway logs

# Heroku
heroku logs --tail
```

**Watch for:**
- `Payment initiated:` - Customer starting payment
- `Collection initiated:` - STK push sent
- `Webhook received:` - Payment confirmed
- `Payout initiated:` - Money sent to driver
- `Payout completed:` - Driver received money

**Admin Dashboard:**
```
https://your-deployed-url.com/admin/dashboard
```

---

## 🐛 Quick Troubleshooting

### Payment fails
- Check wallet has balance
- Verify phone number format: `254XXXXXXXXX`
- Check logs for error messages

### Payout not received
- Ensure "No approval required" set in IntaSend
- Check wallet balance
- Verify driver phone number

### Webhook not working
- Test webhook in IntaSend dashboard
- Check webhook secret matches
- Verify URL is publicly accessible

### API errors
```bash
# Test API connection
python test_production_api.py
```

---

## 📞 Support

- **IntaSend**: support@intasend.com
- **Docs**: See `PRODUCTION_SETUP.md` for detailed guide
- **API Docs**: https://your-deployed-url.com/docs

---

## 🎉 Success!

Your GoPay system is now:
- ✅ Collecting payments automatically
- ✅ Sending payouts to drivers instantly
- ✅ Tracking everything in database
- ✅ Running in production with real money

**Happy deploying! 🚀**


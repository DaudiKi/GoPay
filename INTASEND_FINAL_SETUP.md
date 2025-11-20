# IntaSend Final Setup Guide - Production Ready

**Congratulations!** Your IntaSend account is now verified. Follow these steps to complete the full integration.

---

## 📋 Quick Checklist

- [ ] Step 1: Get IntaSend Production Credentials (5 min)
- [ ] Step 2: Run Database Migration (5 min)
- [ ] Step 3: Configure Environment Variables (5 min)
- [ ] Step 4: Test Locally with Sandbox (15 min)
- [ ] Step 5: Deploy to Production (30 min)
- [ ] Step 6: Configure Webhooks (10 min)
- [ ] Step 7: Switch to Production Keys (5 min)
- [ ] Step 8: Run End-to-End Test (15 min)

**Total Time: ~90 minutes**

---

## Step 1: Get IntaSend Credentials (5 minutes)

### Get API Keys

1. **Login to IntaSend Dashboard**
   - Go to: https://dashboard.intasend.com
   - Login with your verified account

2. **Get Sandbox Keys (for testing)**
   - Navigate to: **Settings → API Keys**
   - Copy your **Sandbox** credentials:
     ```
     ✅ Secret API Key (ISSecretKey_test_...)
     ✅ Publishable Key (ISPubKey_test_...)
     ```

3. **Get Production Keys (for live)**
   - In same page, copy your **Production** credentials:
     ```
     ✅ Secret API Key (ISSecretKey_live_...)
     ✅ Publishable Key (ISPubKey_live_...)
     ```

4. **Save both sets** - You'll need them later

### Enable Required Services

1. **Enable Collections (M-Pesa STK Push)**
   - Go to: **Collections** section
   - Enable: **M-Pesa STK Push**
   - Configure your M-Pesa business details

2. **Enable Payouts (M-Pesa Disbursements)**
   - Go to: **Payouts** section
   - Enable: **M-Pesa Disbursements**
   - Set approval to: **"No approval required"** (for automatic payouts)
   - Add your bank account for funding payouts

---

## Step 2: Run Database Migration (5 minutes)

### Execute in Supabase

1. **Open Supabase Project**
   - Go to: https://supabase.com
   - Open your GoPay project

2. **Open SQL Editor**
   - Click: **SQL Editor** in left sidebar
   - Click: **New Query**

3. **Copy Migration Script**
   - Open file: `database/intasend_migration.sql`
   - Copy entire contents

4. **Execute Migration**
   - Paste in SQL Editor
   - Click: **Run** button
   - Wait for success message

5. **Verify Tables Created**
   Run this query to verify:
   ```sql
   -- Check new tables exist
   SELECT table_name 
   FROM information_schema.tables 
   WHERE table_schema = 'public' 
   AND table_name IN ('payouts', 'platform_fees');
   
   -- Check new columns in transactions
   SELECT column_name 
   FROM information_schema.columns 
   WHERE table_name = 'transactions' 
   AND column_name LIKE '%intasend%';
   ```
   
   ✅ You should see: `payouts` and `platform_fees` tables
   ✅ You should see: Several `intasend_*` columns

---

## Step 3: Configure Environment Variables (5 minutes)

### Create .env File

1. **Copy Template**
   ```bash
   cp env.intasend.example .env
   ```

2. **Edit .env File**
   Open `.env` and update with your credentials:

   ```env
   # Application Settings
   BASE_PUBLIC_URL=http://localhost:8000
   
   # Supabase Configuration (KEEP YOUR EXISTING VALUES)
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your-supabase-anon-key-here
   
   # IntaSend API Configuration - SANDBOX (for testing)
   INTASEND_API_KEY=ISSecretKey_test_YOUR_KEY_HERE
   INTASEND_PUBLISHABLE_KEY=ISPubKey_test_YOUR_KEY_HERE
   
   # IntaSend Environment (use sandbox for testing)
   INTASEND_TEST_MODE=true
   
   # Webhook Secret (leave empty for now, add after deployment)
   INTASEND_WEBHOOK_SECRET=
   
   # Platform Fee Configuration
   PLATFORM_FEE_PERCENTAGE=0.5  # 0.5% commission
   PLATFORM_FEE_FIXED=0         # No fixed fee
   ```

3. **Important Notes:**
   - Start with **SANDBOX** keys (`INTASEND_TEST_MODE=true`)
   - Keep your existing Supabase credentials
   - Don't commit `.env` to git (already in `.gitignore`)

---

## Step 4: Test Locally with Sandbox (15 minutes)

### Start Application

1. **Install Dependencies** (if not already done)
   ```bash
   pip install -r requirements.txt
   ```

2. **Start IntaSend-enabled Application**
   ```bash
   uvicorn app.main_intasend:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Verify Application Started**
   - Open: http://localhost:8000
   - You should see: GoPay welcome page
   - Open: http://localhost:8000/docs
   - You should see: API documentation

### Register Test Driver

```bash
curl -X POST http://localhost:8000/api/register_driver \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Driver",
    "phone": "254722000000",
    "email": "driver@test.com",
    "vehicle_type": "boda",
    "vehicle_number": "KBW 123T"
  }'
```

✅ **Expected Response:**
```json
{
  "status": "success",
  "driver_id": "uuid-here",
  "qr_code_url": "https://...",
  "message": "Driver registered successfully"
}
```

📝 **Save the `driver_id`** - you'll need it for testing

### Test Payment Flow

1. **Open Payment Page**
   ```
   http://localhost:8000/pay?driver_id=YOUR_DRIVER_ID&phone=254722000001
   ```

2. **Test Payment Form**
   - Enter amount: `100`
   - Phone should be pre-filled: `254722000001`
   - See fee breakdown displayed
   - Click: **Pay Now**

3. **Check Logs**
   Watch your terminal for:
   ```
   INFO: Payment initiated: 100.0 KES - Fee: 0.5 - Driver: 99.5
   INFO: Transaction created: transaction-id
   INFO: Collection initiated. ID: col_xxx
   ```

### Test Webhook Manually (Local Testing)

Since webhooks won't reach localhost, simulate manually:

```bash
curl -X POST http://localhost:8000/api/webhooks/intasend \
  -H "Content-Type: application/json" \
  -d '{
    "state": "COMPLETE",
    "api_ref": "YOUR_TRANSACTION_ID",
    "value": 100,
    "charges": 0,
    "net_amount": 100,
    "currency": "KES",
    "provider": "M-PESA"
  }'
```

✅ **Check Logs Should Show:**
```
INFO: Webhook received: COMPLETE - YOUR_TRANSACTION_ID
INFO: Payment collected. Payout scheduled for 99.5 KES
INFO: Processing payout for transaction YOUR_TRANSACTION_ID
INFO: Payout initiated successfully. Tracking ID: pay_xxx
```

### Verify in Database

Open Supabase and check:

```sql
-- View transaction
SELECT * FROM transactions ORDER BY created_at DESC LIMIT 1;

-- View payout
SELECT * FROM payouts ORDER BY created_at DESC LIMIT 1;

-- View platform fee
SELECT * FROM platform_fees ORDER BY created_at DESC LIMIT 1;
```

✅ **All tables should have new records**

---

## Step 5: Deploy to Production (30 minutes)

### Choose Hosting Platform

Popular options:
- **Railway** (Recommended - Easy setup)
- **Render**
- **Heroku**
- **DigitalOcean App Platform**
- **Your own VPS**

### Deploy Application

I'll show Railway as example:

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize Project**
   ```bash
   railway init
   ```

4. **Add Environment Variables**
   ```bash
   railway variables set SUPABASE_URL="your-value"
   railway variables set SUPABASE_ANON_KEY="your-value"
   railway variables set INTASEND_API_KEY="ISSecretKey_test_xxx"
   railway variables set INTASEND_PUBLISHABLE_KEY="ISPubKey_test_xxx"
   railway variables set INTASEND_TEST_MODE="true"
   railway variables set PLATFORM_FEE_PERCENTAGE="0.5"
   railway variables set PLATFORM_FEE_FIXED="0"
   railway variables set BASE_PUBLIC_URL="https://your-app.railway.app"
   ```

5. **Deploy**
   ```bash
   railway up
   ```

6. **Get Your Public URL**
   ```bash
   railway domain
   ```
   
   📝 **Save this URL** - Example: `https://gopay-production.railway.app`

### Verify Deployment

1. **Test Health Endpoint**
   ```bash
   curl https://your-app.railway.app/health
   ```
   
   ✅ Should return: `{"status":"healthy","service":"GoPay IntaSend","version":"2.0.0"}`

2. **Test API Docs**
   - Open: https://your-app.railway.app/docs
   - Should see: Interactive API documentation

---

## Step 6: Configure Webhooks (10 minutes)

### Add Webhook in IntaSend Dashboard

1. **Login to IntaSend Dashboard**
   - Go to: https://dashboard.intasend.com
   - Navigate to: **Settings → Webhooks**

2. **Add New Webhook**
   - Click: **Add Webhook**
   - Enter URL: `https://your-app.railway.app/api/webhooks/intasend`
   - Select Events:
     - ✅ **Payment Completed**
     - ✅ **Payment Failed**
     - ✅ **Payout Completed**
     - ✅ **Payout Failed**
   - Click: **Save**

3. **Copy Webhook Secret**
   - After saving, IntaSend generates a webhook secret
   - Copy it: `whs_abc123xyz...`

4. **Add Secret to Production**
   ```bash
   railway variables set INTASEND_WEBHOOK_SECRET="whs_abc123xyz..."
   ```

5. **Test Webhook**
   - In IntaSend dashboard, click: **Test Webhook**
   - Send test event
   - Check your application logs
   - Should see: `INFO: Webhook received: ...`

---

## Step 7: Switch to Production Keys (5 minutes)

**ONLY DO THIS WHEN READY TO GO LIVE**

### Update Environment Variables

1. **Get Production Keys from IntaSend**
   - Dashboard → Settings → API Keys
   - Copy **Production** keys (not sandbox)

2. **Update Production Environment**
   ```bash
   railway variables set INTASEND_API_KEY="ISSecretKey_live_xxx"
   railway variables set INTASEND_PUBLISHABLE_KEY="ISPubKey_live_xxx"
   railway variables set INTASEND_TEST_MODE="false"
   ```

3. **Restart Application**
   ```bash
   railway restart
   ```

### Fund Production Wallet

**IMPORTANT:** Before going live, fund your IntaSend wallet!

1. **Go to IntaSend Dashboard → Wallet**
2. **Add Funds** (bank transfer or M-Pesa)
3. **Verify Balance** sufficient for payouts
4. **Set up auto-reload** if available

---

## Step 8: Run End-to-End Test (15 minutes)

### Test with Real M-Pesa

1. **Register Real Driver**
   ```bash
   curl -X POST https://your-app.railway.app/api/register_driver \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Your Name",
       "phone": "254YOUR_REAL_NUMBER",
       "email": "your@email.com",
       "vehicle_type": "boda",
       "vehicle_number": "KBW 456X"
     }'
   ```

2. **Get QR Code**
   - Save `qr_code_url` from response
   - Open URL in browser
   - Download and print QR code

3. **Make Test Payment**
   - Open payment page: `https://your-app.railway.app/pay?driver_id=YOUR_ID&phone=254YOUR_PHONE`
   - Enter small amount: `50` KES
   - Click: **Pay Now**
   - Check phone for M-Pesa prompt
   - Enter PIN and confirm

4. **Verify Complete Flow**
   - ✅ M-Pesa prompt received
   - ✅ Payment deducted from your account
   - ✅ Webhook received (check logs)
   - ✅ Payout initiated (check logs)
   - ✅ Driver receives payout (check M-Pesa SMS)
   - ✅ Dashboard updated

5. **Check Dashboard**
   - Driver dashboard: `https://your-app.railway.app/driver/YOUR_DRIVER_ID/dashboard`
   - Admin dashboard: `https://your-app.railway.app/admin/dashboard`

---

## 🎉 You're Live!

Your IntaSend integration is now fully operational!

### What Happens Next?

When a passenger scans a driver's QR code:
1. 📱 Payment page loads with driver info
2. 💰 Passenger enters amount and pays via M-Pesa
3. ⚡ IntaSend processes payment
4. 📨 Webhook confirms payment to your server
5. 🤖 System automatically calculates fee
6. 💸 System automatically sends payout to driver
7. 📊 Dashboard updates in real-time

---

## 📊 Monitoring

### Key Things to Monitor

1. **Transaction Success Rate**
   ```sql
   SELECT 
     COUNT(*) FILTER (WHERE collection_status = 'completed') * 100.0 / COUNT(*) as success_rate
   FROM transactions 
   WHERE created_at > NOW() - INTERVAL '24 hours';
   ```

2. **Average Payout Time**
   ```sql
   SELECT 
     AVG(payout_completed_at - collection_completed_at) as avg_payout_time
   FROM transactions
   WHERE payout_status = 'completed';
   ```

3. **Platform Revenue Today**
   ```sql
   SELECT SUM(amount) as today_revenue
   FROM platform_fees
   WHERE collected_at >= CURRENT_DATE;
   ```

4. **Failed Transactions**
   ```sql
   SELECT * FROM transactions 
   WHERE status = 'failed' 
   OR payout_status = 'failed'
   ORDER BY created_at DESC;
   ```

### Application Logs

Monitor your Railway logs:
```bash
railway logs
```

Look for:
- ✅ `Payment initiated`
- ✅ `Collection initiated`
- ✅ `Webhook received`
- ✅ `Payout initiated successfully`
- ✅ `Payout completed`
- ❌ Any errors or warnings

---

## 🆘 Troubleshooting

### Issue: Webhook Not Received

**Solutions:**
1. Verify webhook URL is publicly accessible
2. Test with: `curl https://your-app.railway.app/api/webhooks/intasend`
3. Check IntaSend dashboard → Webhooks → Logs
4. Verify webhook secret matches
5. Check application logs for errors

### Issue: Payout Not Initiating

**Solutions:**
1. Check IntaSend wallet balance
2. Verify payout permissions enabled in IntaSend
3. Check application logs for payout errors
4. Verify driver phone number format (254XXXXXXXXX)
5. Check payout status in database

### Issue: Payment Stuck in Pending

**Solutions:**
1. Check if webhook was received (logs)
2. Manually check status in IntaSend dashboard
3. Query transaction in database
4. Simulate webhook if needed (see Step 4)

### Issue: IntaSend API Error 401

**Solutions:**
1. Verify API key is correct (no spaces)
2. Check if using correct environment (test vs live)
3. Verify key hasn't expired
4. Regenerate keys in IntaSend dashboard if needed

---

## 📚 Next Steps

1. **Train Your Team**
   - Share driver registration process
   - Explain payment flow to drivers
   - Set up support process

2. **Create Driver Documentation**
   - How to get their QR code
   - How to check earnings
   - How payouts work

3. **Set Up Monitoring**
   - Set up error alerting
   - Create daily reports
   - Monitor wallet balance

4. **Optimize**
   - Gather user feedback
   - Analyze transaction patterns
   - Adjust fees if needed

---

## 📞 Support

### IntaSend Support
- Email: support@intasend.com
- Docs: https://developers.intasend.com
- Dashboard: https://dashboard.intasend.com

### Application Issues
- Check logs: `railway logs`
- API docs: `https://your-app.railway.app/docs`
- Database: Supabase dashboard

---

**Congratulations! Your GoPay with IntaSend integration is complete! 🚀**


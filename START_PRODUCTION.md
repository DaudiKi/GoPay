# 🚀 Start Here: Production Deployment

**Your IntaSend account is verified!** Let's get GoPay live in production.

---

## 📍 Where You Are Now

✅ **Completed:**
- IntaSend account verified
- Code fully implemented
- Sandbox testing ready
- Production configuration files created

⏳ **Next Steps:**
- Get production API keys
- Deploy to hosting
- Configure webhooks
- Go live!

---

## 🎯 Choose Your Path

### Path 1: Quick Deploy (40 minutes) ⚡

**For:** Getting live fast with minimal complexity

**Follow:** `QUICK_PRODUCTION_DEPLOY.md`

This guide walks you through:
1. Get production keys (5 min)
2. Configure environment (5 min)
3. Test API locally (2 min)
4. Deploy to Railway/Heroku (15 min)
5. Setup webhook (5 min)
6. Fund wallet (5 min)
7. Test end-to-end (5 min)

```bash
# Open quick deploy guide
cat QUICK_PRODUCTION_DEPLOY.md
```

---

### Path 2: Detailed Setup (1-2 hours) 📚

**For:** Understanding every step, custom deployment

**Follow:** `PRODUCTION_SETUP.md`

Comprehensive guide with:
- Detailed explanations
- Multiple deployment options
- Troubleshooting tips
- Best practices
- Monitoring setup

```bash
# Open detailed guide
cat PRODUCTION_SETUP.md
```

---

### Path 3: Checklist-Based (Use alongside other paths) ✅

**For:** Tracking progress step-by-step

**Follow:** `PRODUCTION_CHECKLIST.md`

Checkbox-style checklist covering:
- Every deployment step
- Verification points
- Testing procedures
- Go-live criteria

```bash
# Open checklist
cat PRODUCTION_CHECKLIST.md
```

---

## 🔧 Before You Start

### Required Tools

**Already Installed:**
- ✅ Python 3.8+
- ✅ pip
- ✅ git

**Need to Install (choose based on hosting):**

**For Railway:**
```bash
npm install -g @railway/cli
```

**For Heroku:**
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Required Accounts

- ✅ IntaSend account (verified)
- ✅ Supabase account
- [ ] Hosting account (Railway/Heroku/VPS)

---

## 🚦 Quick Start Commands

### Step 1: Get Production Keys

1. Go to: https://dashboard.intasend.com
2. Switch to **PRODUCTION** mode
3. Settings → API Keys
4. Copy both keys

### Step 2: Configure Environment

```bash
# Copy production template
cp env.production.example .env.production

# Edit with your keys
nano .env.production
# (or use your preferred editor)
```

Update these values:
- `INTASEND_API_KEY` → Your production secret key
- `INTASEND_PUBLISHABLE_KEY` → Your production publishable key
- `INTASEND_TEST_MODE` → Set to `false`
- `SUPABASE_URL` → Your Supabase project URL
- `SUPABASE_ANON_KEY` → Your Supabase anon key

### Step 3: Test Locally

```bash
# Test database
python verify_database.py

# Test API connection
python test_production_api.py
```

Both should show: **✅ Success**

### Step 4: Deploy

**Railway (Recommended):**
```bash
railway login
railway init
railway up
railway domain  # Get your URL
```

**Heroku:**
```bash
heroku login
heroku create gopay-production
git push heroku master
```

### Step 5: Configure

```bash
# Set environment variables (Railway example)
railway variables set INTASEND_API_KEY="your-key"
railway variables set INTASEND_PUBLISHABLE_KEY="your-pub-key"
railway variables set INTASEND_TEST_MODE="false"
# ... set all other variables
```

### Step 6: Setup Webhook

1. IntaSend Dashboard → Webhooks
2. Add: `https://your-deployed-url.com/api/webhooks/intasend`
3. Enable all payment & payout events
4. Copy webhook secret
5. Add to environment: `INTASEND_WEBHOOK_SECRET`

### Step 7: Fund Wallet

1. IntaSend Dashboard → Wallet
2. Add Funds (via M-Pesa)
3. Start with 10,000+ KES

### Step 8: Test!

```bash
# Register test driver
curl -X POST https://your-url.com/api/register_driver \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","phone":"254712345678","email":"test@test.com","vehicle_type":"boda","vehicle_number":"TEST"}'

# Open payment page on phone
# Make 10 KES test payment
# Verify payout received
```

---

## 📊 What Happens Next?

### Automatic Flow

1. **Passenger scans QR** → Opens payment page
2. **Makes payment** → STK push to phone
3. **Payment collected** → Webhook triggers
4. **Platform fee deducted** → Tracked in database
5. **Payout initiated** → Money sent to driver
6. **Driver receives** → M-Pesa SMS confirmation
7. **Everything logged** → View in dashboards

### You Can Monitor

**Admin Dashboard:**
```
https://your-domain.com/admin/dashboard
```

**Driver Dashboard:**
```
https://your-domain.com/driver/DRIVER_ID/dashboard
```

**API Documentation:**
```
https://your-domain.com/docs
```

**Logs:**
```bash
# Railway
railway logs

# Heroku
heroku logs --tail
```

---

## 🆘 Need Help?

### Test Scripts Available

```bash
# Test database migration
python verify_database.py

# Test API connection
python test_production_api.py
```

### Documentation

- `QUICK_PRODUCTION_DEPLOY.md` - Fast deployment guide
- `PRODUCTION_SETUP.md` - Detailed setup guide
- `PRODUCTION_CHECKLIST.md` - Step-by-step checklist
- `INTASEND_IMPLEMENTATION.md` - Technical details
- `INTASEND_SETUP.md` - IntaSend configuration

### Support

**IntaSend Issues:**
- Email: support@intasend.com
- Dashboard: https://dashboard.intasend.com

**Application Issues:**
- Check logs
- Review documentation
- Test with sandbox mode first

---

## ⚠️ Important Reminders

1. **Test Mode = False**: In production, `INTASEND_TEST_MODE=false`
2. **Production Keys**: Use keys starting with `_live_`, not `_test_`
3. **Fund Wallet**: Need balance for payouts to work
4. **HTTPS Required**: Webhooks only work with HTTPS
5. **Test First**: Always test with small amounts (10 KES)

---

## 🎉 You're Ready!

Pick your path above and let's get GoPay live!

**Estimated Time to Production:**
- Quick path: 40 minutes
- Detailed path: 1-2 hours

**Questions?** Check the detailed guides for answers.

**Let's deploy! 🚀**

---

## 📋 Quick Reference

| Need | Command | Documentation |
|------|---------|--------------|
| Test database | `python verify_database.py` | PRODUCTION_SETUP.md |
| Test API | `python test_production_api.py` | QUICK_PRODUCTION_DEPLOY.md |
| Deploy Railway | `railway up` | QUICK_PRODUCTION_DEPLOY.md |
| Deploy Heroku | `git push heroku master` | PRODUCTION_SETUP.md |
| View logs | `railway logs` or `heroku logs --tail` | Platform docs |
| Check health | Visit `/health` endpoint | API docs |



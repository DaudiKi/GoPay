# 🚀 Quick Start: GoPay with IntaSend

**Your IntaSend account is verified! Let's get you live in 15 minutes.**

---

## 📍 Where You Are

✅ IntaSend account created and verified
✅ All code files ready (`app/intasend.py`, `app/main_intasend.py`, etc.)
✅ Database migration script ready

---

## ⚡ 15-Minute Setup

### Step 1: Get Your Keys (2 min)

1. Login: https://dashboard.intasend.com
2. Go to: **Settings → API Keys**
3. Copy **Sandbox** keys (for testing):
   - Secret API Key: `ISSecretKey_test_...`
   - Publishable Key: `ISPubKey_test_...`

### Step 2: Setup Database (3 min)

1. Open: https://supabase.com (your project)
2. Click: **SQL Editor** → **New Query**
3. Copy & paste: `database/intasend_migration.sql`
4. Click: **Run**
5. ✅ Success!

### Step 3: Configure Environment (2 min)

```bash
# Create .env file
cp env.intasend.example .env

# Edit .env with your credentials
# Update these lines:
SUPABASE_URL=https://YOUR-PROJECT.supabase.co
SUPABASE_ANON_KEY=your-key-here
INTASEND_API_KEY=ISSecretKey_test_YOUR_KEY
INTASEND_PUBLISHABLE_KEY=ISPubKey_test_YOUR_KEY
INTASEND_TEST_MODE=true
```

### Step 4: Install & Verify (3 min)

```bash
# Install dependencies
pip install -r requirements.txt

# Verify setup
python verify_intasend_setup.py
```

✅ All checks should pass

### Step 5: Start Application (1 min)

```bash
# Start server
uvicorn app.main_intasend:app --reload --host 0.0.0.0 --port 8000
```

Open: http://localhost:8000

### Step 6: Test It! (4 min)

**Register test driver:**
```bash
curl -X POST http://localhost:8000/api/register_driver \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Driver",
    "phone": "254722000000",
    "email": "test@driver.com",
    "vehicle_type": "boda",
    "vehicle_number": "KBW 123T"
  }'
```

**Open payment page:**
```
http://localhost:8000/pay?driver_id=YOUR_ID&phone=254722000001
```

**Test payment:** Enter 100 KES and click Pay Now

✅ You're running!

---

## 🎯 What Just Happened?

When a passenger pays:
1. 💰 IntaSend collects payment via M-Pesa
2. 🤖 System automatically calculates fee (0.5%)
3. 💸 System automatically sends payout to driver
4. 📊 Dashboard updates in real-time

**Example:**
- Passenger pays: 100 KES
- Platform fee: 0.50 KES
- Driver receives: 99.50 KES (automatically!)

---

## 📋 What's Next?

### For Local Testing:
✅ You're done! Keep testing with sandbox

### To Deploy to Production:

**Quick Path:**
1. Deploy to Railway/Render
2. Configure webhooks in IntaSend
3. Switch to production keys
4. Fund your IntaSend wallet
5. Test with real money

**Detailed Guide:** See `INTASEND_FINAL_SETUP.md`

---

## 🆘 Quick Troubleshooting

**Application won't start?**
```bash
# Check environment variables
python verify_intasend_setup.py
```

**Database errors?**
- Run migration: `database/intasend_migration.sql` in Supabase SQL Editor

**IntaSend errors?**
- Verify API keys in `.env`
- Check if using correct mode (test vs live)

**Payment not working?**
- Check logs in terminal
- Use sandbox test numbers: 254722000000, 254722000001
- Verify webhook received (check logs)

---

## 📚 All Documentation

| File | Purpose |
|------|---------|
| `INTASEND_FINAL_SETUP.md` | Complete step-by-step production setup |
| `PRODUCTION_DEPLOYMENT_CHECKLIST.md` | Full deployment checklist |
| `INTASEND_IMPLEMENTATION.md` | Technical implementation details |
| `INTASEND_SETUP.md` | Detailed IntaSend account setup |
| `MIGRATION_CHECKLIST.md` | Migration from old system |
| `verify_intasend_setup.py` | Automated setup verification |
| `quick_start.sh` | Automated quick start script |

---

## 🎊 Key Features Now Available

✅ **Automatic Payment Collection** - M-Pesa STK Push
✅ **Instant Driver Payouts** - Money sent automatically
✅ **Platform Fee Management** - Configurable commission
✅ **Real-time Webhooks** - Instant notifications
✅ **QR Code Payments** - Easy passenger experience
✅ **Transaction Tracking** - Complete audit trail
✅ **Admin Dashboard** - Platform statistics
✅ **Driver Dashboard** - Earnings and history

---

## 💡 Pro Tips

1. **Always test in sandbox first** (`INTASEND_TEST_MODE=true`)
2. **Monitor logs closely** during first transactions
3. **Fund wallet before production** (at least 50,000 KES)
4. **Set up webhooks immediately** after deployment
5. **Keep API keys secure** (never commit to git)

---

## 📞 Need Help?

**IntaSend Support:**
- Email: support@intasend.com
- Docs: https://developers.intasend.com

**Check Documentation:**
- API docs: http://localhost:8000/docs
- Implementation guide: `INTASEND_IMPLEMENTATION.md`
- Troubleshooting: `INTASEND_SETUP.md` (section 10)

---

## ✅ Success Checklist

- [ ] IntaSend sandbox keys configured
- [ ] Database migration executed
- [ ] Application starts without errors
- [ ] Test driver registered successfully
- [ ] Payment flow tested
- [ ] Webhook handling verified
- [ ] Ready to deploy!

---

**You're all set! Happy coding! 🎉**

For detailed production deployment, see `INTASEND_FINAL_SETUP.md`


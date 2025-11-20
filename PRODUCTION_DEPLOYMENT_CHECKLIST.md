# Production Deployment Checklist

Use this checklist to ensure a smooth deployment to production.

---

## ☑️ Pre-Deployment Preparation

### Account Setup
- [ ] IntaSend account created and verified
- [ ] KYC documents submitted and approved
- [ ] Business registration completed
- [ ] Bank account linked to IntaSend

### Credentials Collection
- [ ] Supabase URL and Anon Key copied
- [ ] IntaSend Sandbox API Key copied
- [ ] IntaSend Sandbox Publishable Key copied
- [ ] IntaSend Production API Key copied (save for later)
- [ ] IntaSend Production Publishable Key copied (save for later)

### Local Testing
- [ ] Database migration executed successfully
- [ ] `.env` file configured with sandbox keys
- [ ] Application runs locally without errors
- [ ] Test driver registered successfully
- [ ] QR code generated and accessible
- [ ] Payment flow tested manually
- [ ] Webhook simulation successful
- [ ] Database records verified

---

## ☑️ Database Setup

### Supabase Configuration
- [ ] Supabase project created
- [ ] SQL migration executed (`database/intasend_migration.sql`)
- [ ] All tables created successfully:
  - [ ] `drivers`
  - [ ] `transactions`
  - [ ] `payouts`
  - [ ] `platform_fees`
  - [ ] `admin_stats`
- [ ] Row Level Security (RLS) enabled on tables
- [ ] Storage bucket `qr-codes` created
- [ ] Storage bucket is public
- [ ] Database backup configured

### Verification Queries
Run these to verify database setup:

```sql
-- Check all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('drivers', 'transactions', 'payouts', 'platform_fees', 'admin_stats');

-- Check IntaSend columns exist
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'transactions' 
AND column_name LIKE '%intasend%';

-- Check triggers
SELECT trigger_name, event_object_table 
FROM information_schema.triggers 
WHERE event_object_schema = 'public';
```

---

## ☑️ IntaSend Configuration

### Dashboard Settings
- [ ] Collections (M-Pesa STK Push) enabled
- [ ] Payouts (M-Pesa Disbursements) enabled
- [ ] Payout approval set to "No approval required"
- [ ] M-Pesa business details configured
- [ ] Settlement account configured

### Wallet Setup
- [ ] Production wallet funded
- [ ] Sufficient balance for initial payouts (recommended: at least 50,000 KES)
- [ ] Auto-reload configured (if available)
- [ ] Alert notifications enabled for low balance

---

## ☑️ Application Deployment

### Hosting Platform Selection
Choose one:
- [ ] Railway (Recommended - Easy setup)
- [ ] Render
- [ ] Heroku
- [ ] DigitalOcean App Platform
- [ ] AWS/GCP/Azure
- [ ] Your own VPS

### Deployment Steps (Railway Example)
- [ ] Railway CLI installed
- [ ] Railway account created
- [ ] Project initialized
- [ ] GitHub repository connected (optional)
- [ ] Environment variables configured
- [ ] Application deployed
- [ ] Public URL obtained
- [ ] Custom domain connected (optional)
- [ ] SSL certificate active (HTTPS)

### Environment Variables Checklist
Verify all environment variables set:

```bash
# Application
✓ BASE_PUBLIC_URL

# Supabase
✓ SUPABASE_URL
✓ SUPABASE_ANON_KEY

# IntaSend (use sandbox first)
✓ INTASEND_API_KEY
✓ INTASEND_PUBLISHABLE_KEY
✓ INTASEND_TEST_MODE=true

# Webhook (add after webhook configuration)
✓ INTASEND_WEBHOOK_SECRET

# Fees
✓ PLATFORM_FEE_PERCENTAGE
✓ PLATFORM_FEE_FIXED
```

### Deployment Verification
- [ ] Application accessible via public URL
- [ ] Health endpoint responds: `/health`
- [ ] API docs accessible: `/docs`
- [ ] Homepage loads: `/`
- [ ] Static files loading (CSS, images)
- [ ] No errors in deployment logs

---

## ☑️ Webhook Configuration

### Setup in IntaSend
- [ ] Logged into IntaSend dashboard
- [ ] Navigated to Settings → Webhooks
- [ ] Webhook URL added: `https://your-app.com/api/webhooks/intasend`
- [ ] Events selected:
  - [ ] Payment Completed
  - [ ] Payment Failed
  - [ ] Payout Completed
  - [ ] Payout Failed
- [ ] Webhook secret generated
- [ ] Webhook secret added to environment variables
- [ ] Application restarted after adding secret

### Webhook Testing
- [ ] Test webhook sent from IntaSend dashboard
- [ ] Webhook received in application logs
- [ ] Webhook signature validated successfully
- [ ] Test webhook processed without errors

---

## ☑️ Sandbox Testing (Production Environment)

### Test Complete Flow
- [ ] Register test driver with real phone number
- [ ] QR code generated and downloadable
- [ ] Payment page accessible via QR scan
- [ ] Test payment initiated (small amount)
- [ ] M-Pesa prompt received on phone
- [ ] Payment completed successfully
- [ ] Webhook received and processed
- [ ] Platform fee recorded correctly
- [ ] Payout initiated automatically
- [ ] Payout completed successfully
- [ ] Driver received M-Pesa confirmation
- [ ] Transaction visible in driver dashboard
- [ ] Transaction visible in admin dashboard
- [ ] All database records created correctly

### Verify Calculations
Test with known amounts:

| Amount | Expected Fee (0.5%) | Expected Driver Amount |
|--------|---------------------|------------------------|
| 100    | 0.50               | 99.50                  |
| 500    | 2.50               | 497.50                 |
| 1000   | 5.00               | 995.00                 |

- [ ] Fee calculations match expectations
- [ ] Driver receives correct amount
- [ ] Platform fee recorded correctly

---

## ☑️ Switch to Production Mode

**⚠️ ONLY DO THIS AFTER SUCCESSFUL SANDBOX TESTING**

### Update Environment Variables
- [ ] INTASEND_API_KEY changed to production key
- [ ] INTASEND_PUBLISHABLE_KEY changed to production key
- [ ] INTASEND_TEST_MODE changed to `false`
- [ ] Application restarted
- [ ] Deployment logs checked for errors

### Production Webhook Update
- [ ] Webhook URL updated to production endpoint (if different)
- [ ] Webhook secret verified
- [ ] Test webhook sent
- [ ] Production webhook working

---

## ☑️ Production Testing

### Initial Production Transaction
- [ ] Small test amount used (e.g., 50 KES)
- [ ] Real M-Pesa payment made
- [ ] Payment collected successfully
- [ ] Webhook received
- [ ] Payout completed
- [ ] Driver received real money
- [ ] All logs reviewed
- [ ] No errors encountered

### Multiple Transaction Test
- [ ] 3-5 transactions completed
- [ ] Different amounts tested
- [ ] Multiple drivers tested (if available)
- [ ] All payouts successful
- [ ] Dashboard statistics accurate
- [ ] Platform fees calculated correctly

---

## ☑️ Monitoring Setup

### Application Monitoring
- [ ] Error tracking configured (Sentry, LogRocket, etc.)
- [ ] Log aggregation set up
- [ ] Uptime monitoring active (UptimeRobot, Pingdom, etc.)
- [ ] Performance monitoring enabled

### Alerts Configuration
Set up alerts for:
- [ ] Application downtime
- [ ] Failed transactions
- [ ] Failed payouts
- [ ] Webhook failures
- [ ] Low IntaSend wallet balance
- [ ] High error rate
- [ ] API rate limit approaching

### Database Monitoring
- [ ] Supabase monitoring enabled
- [ ] Database backup schedule configured
- [ ] Query performance monitoring active
- [ ] Storage usage alerts set

---

## ☑️ Security Checklist

### Application Security
- [ ] HTTPS enabled (SSL certificate active)
- [ ] Environment variables not exposed in code
- [ ] `.env` file in `.gitignore`
- [ ] API keys not committed to git
- [ ] Webhook signature validation enabled
- [ ] CORS configured properly
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (parameterized queries)

### Access Control
- [ ] Admin dashboard protected (if applicable)
- [ ] Supabase RLS policies configured
- [ ] API authentication implemented (if needed)
- [ ] Sensitive data encrypted
- [ ] Logs don't contain sensitive information

---

## ☑️ Documentation

### Internal Documentation
- [ ] API endpoints documented
- [ ] Environment setup documented
- [ ] Deployment process documented
- [ ] Troubleshooting guide created
- [ ] Database schema documented

### User Documentation
- [ ] Driver registration guide
- [ ] Driver onboarding instructions
- [ ] How to use QR codes
- [ ] How to check earnings
- [ ] Payout schedule explained
- [ ] FAQ document created

### Support Documentation
- [ ] Common issues documented
- [ ] Support contact information
- [ ] Escalation process defined
- [ ] Refund process documented (if applicable)

---

## ☑️ Team Preparation

### Training
- [ ] Support team trained on system
- [ ] Support team knows how to check transactions
- [ ] Support team can access dashboards
- [ ] Support team knows escalation process

### Communication
- [ ] Drivers notified of new system
- [ ] Launch announcement prepared
- [ ] Support channels established
- [ ] Emergency contact list created

---

## ☑️ Go-Live Checklist

### Final Verification (Day of Launch)
- [ ] All systems operational
- [ ] IntaSend wallet funded
- [ ] No critical errors in logs
- [ ] Backup plan ready
- [ ] Support team standing by
- [ ] Monitoring dashboards open
- [ ] Emergency contacts available

### Launch
- [ ] Announcement sent
- [ ] System made available to drivers
- [ ] First transactions monitored closely
- [ ] Quick response to any issues

### Post-Launch (First 24 Hours)
- [ ] Monitor all transactions
- [ ] Check webhook delivery rate
- [ ] Verify payout success rate
- [ ] Review error logs
- [ ] Gather initial feedback
- [ ] Address any urgent issues

### Post-Launch (First Week)
- [ ] Review success metrics
- [ ] Analyze transaction patterns
- [ ] Check platform revenue
- [ ] Verify payout timings
- [ ] Address user feedback
- [ ] Optimize as needed
- [ ] Document lessons learned

---

## ☑️ Success Metrics

Track these metrics after launch:

### Performance Metrics
- [ ] Payment success rate > 95%
- [ ] Average payout time < 2 minutes
- [ ] Webhook delivery rate > 99%
- [ ] Application uptime > 99.9%
- [ ] API response time < 500ms

### Business Metrics
- [ ] Number of active drivers
- [ ] Daily transaction volume
- [ ] Total revenue processed
- [ ] Platform fees collected
- [ ] Average transaction size
- [ ] Driver satisfaction score

---

## 🆘 Rollback Plan

If critical issues arise:

### Immediate Actions
- [ ] Stop new driver registrations
- [ ] Switch back to test mode if needed
- [ ] Communicate issue to users
- [ ] Investigate root cause
- [ ] Fix in staging environment

### Recovery Steps
- [ ] Test fix thoroughly
- [ ] Deploy fix to production
- [ ] Verify fix working
- [ ] Resume normal operations
- [ ] Post-mortem analysis
- [ ] Update documentation

---

## 📊 Regular Maintenance

### Daily
- [ ] Check error logs
- [ ] Monitor transaction success rate
- [ ] Verify wallet balance
- [ ] Review failed payouts

### Weekly
- [ ] Analyze transaction trends
- [ ] Review platform revenue
- [ ] Check system performance
- [ ] Update documentation if needed

### Monthly
- [ ] Review success metrics
- [ ] Analyze user feedback
- [ ] Plan optimizations
- [ ] Update team on performance
- [ ] Review and adjust fees if needed

---

## ✅ Deployment Complete!

When all items are checked:
- [ ] **All checklist items completed**
- [ ] **Production system verified**
- [ ] **Team trained and ready**
- [ ] **Monitoring active**
- [ ] **Documentation complete**

**Congratulations! Your GoPay system is now live in production! 🎉**

---

## 📞 Emergency Contacts

**IntaSend Support:**
- Email: support@intasend.com
- Phone: +254 xxx xxx xxx
- Dashboard: https://dashboard.intasend.com

**Hosting Support:**
- Railway: https://railway.app/help
- [Your hosting platform support]

**Internal Team:**
- Tech Lead: [Name, Contact]
- DevOps: [Name, Contact]
- Support Lead: [Name, Contact]

---

**Last Updated:** [Current Date]
**Deployment Date:** [To be filled]
**Deployed By:** [Your Name]


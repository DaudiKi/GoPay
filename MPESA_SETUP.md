# M-Pesa Buy Goods Till Number Setup Guide

## Overview
This guide will help you set up a Buy Goods Till number for your GoPay transport service. A Buy Goods Till number is ideal for transport payments because it offers:
- Instant settlement
- Lower transaction fees
- Simple payment flow for customers
- Full API integration support

## Prerequisites
1. Business Registration Documents:
   - Business Registration Certificate or Permit
   - KRA PIN Certificate
   - ID/Passport of business owner

2. Bank Account:
   - Active business bank account
   - Bank statements (last 3 months)

## Step-by-Step Setup Process

### 1. Safaricom Business Registration
1. Visit any Safaricom Shop with:
   - Original ID/Passport
   - Business Registration Certificate
   - KRA PIN Certificate
   - Bank account details
   - Utility bill (for address verification)

2. Request for:
   - Safaricom Business Account
   - Lipa Na M-Pesa Buy Goods Till number

### 2. Till Number Application
1. Fill out the Lipa Na M-Pesa application form:
   - Business details
   - Owner information
   - Bank account details
   - Expected transaction volumes
   - Business location details

2. Choose settlement options:
   - Real-time settlement (recommended)
   - Next day settlement
   - Weekly settlement

### 3. Documentation Verification (1-3 business days)
Safaricom will verify:
- Business registration
- Bank account details
- Physical location
- KYC documents

### 4. Till Number Activation
Once approved:
1. Receive Till Number credentials:
   - Till Number
   - Store Name
   - API credentials (for integration)

2. Sign service agreement:
   - Transaction fees
   - Settlement terms
   - Service level agreement

### 5. System Integration

1. Update `.env` file with new credentials:
```env
# M-Pesa Till Configuration
DARAJA_BASE_URL=https://api.safaricom.com  # Change from sandbox
DARAJA_CONSUMER_KEY=<your_consumer_key>
DARAJA_CONSUMER_SECRET=<your_consumer_secret>
DARAJA_SHORT_CODE=<your_till_number>
DARAJA_PASSKEY=<your_passkey>
DARAJA_CALLBACK_URL=https://your-domain.com/api/mpesa/callback
DARAJA_ACCOUNT_REF=GoPay
DARAJA_TRANSACTION_DESC=Transport Payment
```

2. Update API endpoints:
   - Change from sandbox to production URLs
   - Update callback URLs to your domain
   - Test end-to-end payment flow

## Transaction Fees (as of 2024)
1. Customer Charges:
   - 0-100: Free
   - 101-500: KES 6
   - 501-2,500: KES 12
   - 2,501-70,000: KES 32

2. Business Charges:
   - 0.5% of transaction value
   - Capped at KES 200 per transaction
   - Real-time settlement fee: 0.1% (optional)

## Best Practices
1. **Display Till Number:**
   - Show Till Number clearly on driver's profile
   - Include in payment instructions
   - Add to receipts/confirmation messages

2. **Payment Flow:**
   - Use STK Push for best user experience
   - Include clear payment instructions
   - Show transaction status updates

3. **Reconciliation:**
   - Monitor settlements daily
   - Keep transaction records
   - Regular reconciliation with bank statements

4. **Customer Support:**
   - Save M-Pesa support contacts
   - Train drivers on payment verification
   - Document dispute resolution process

## Support Contacts
- Safaricom Business Support: 0722 002 222
- M-Pesa Business Support: 0722 003 333
- Technical Support Email: api.support@safaricom.co.ke

## Troubleshooting
1. Payment Delays:
   - Check network connectivity
   - Verify transaction status via API
   - Contact M-Pesa support if needed

2. Settlement Issues:
   - Verify bank account details
   - Check transaction reconciliation
   - Contact business support

3. API Integration:
   - Validate API credentials
   - Check callback URL configuration
   - Monitor error logs

## Next Steps After Setup
1. Train drivers on:
   - Payment verification
   - Transaction monitoring
   - Issue reporting

2. Create customer guides for:
   - Payment instructions
   - Transaction verification
   - Support contacts

3. Regular monitoring of:
   - Transaction success rates
   - Settlement accuracy
   - System performance

## Security Guidelines
1. Protect API credentials
2. Regular password updates
3. Monitor for suspicious activities
4. Keep transaction logs
5. Regular security audits

Remember to keep all credentials secure and never share API keys or passwords. For additional support, contact Safaricom Business Support.

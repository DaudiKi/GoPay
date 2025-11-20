# GoPay Payment Aggregator

A modern payment aggregator system for boda riders and Uber/Bolt drivers with **automatic driver payouts via IntaSend**.

## 🎉 IntaSend Integration Complete!

✅ **Your IntaSend account is verified!** GoPay now features:
- 💳 **Automatic Payment Collection** via M-Pesa STK Push
- 💰 **Instant Driver Payouts** - Drivers paid within minutes
- 🔄 **Automatic Fee Splitting** - Platform commission handled automatically
- 📊 **Real-time Webhooks** - Instant payment notifications

### 🚀 Ready to Deploy?

**Quick Start (40 minutes):**
```bash
# 1. Get production keys from IntaSend Dashboard
# 2. Configure environment
cp env.production.example .env.production

# 3. Test connection
python test_production_api.py

# 4. Deploy
railway up  # or: git push heroku master
```

**📚 Full Guides:**
- [`START_PRODUCTION.md`](START_PRODUCTION.md) - Start here!
- [`QUICK_PRODUCTION_DEPLOY.md`](QUICK_PRODUCTION_DEPLOY.md) - 40-minute deployment
- [`PRODUCTION_SETUP.md`](PRODUCTION_SETUP.md) - Detailed guide
- [`PRODUCTION_CHECKLIST.md`](PRODUCTION_CHECKLIST.md) - Step-by-step checklist

---

## Features

- 🚗 **Driver Registration**: Easy onboarding with QR code generation
- 💳 **M-Pesa Integration**: Seamless mobile money payments
- 📊 **Real-time Dashboards**: For both drivers and administrators
- 📱 **Responsive UI**: Works on all devices
- 🔒 **Secure Transactions**: Built with security best practices
- 📈 **Transaction Tracking**: Complete payment history and analytics

## Tech Stack

- **Backend**: FastAPI (Python async web framework)
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage (for QR codes)
- **Payment Gateway**: IntaSend (M-Pesa STK Push & Payouts)
- **Frontend**: HTML + TailwindCSS + Vanilla JS
- **QR Codes**: qrcode[pil]

### Why IntaSend?

- ✅ Single API for collections AND payouts
- ✅ Automatic webhook notifications
- ✅ No manual payout approval needed
- ✅ Production-ready with KYC verification
- ✅ Comprehensive dashboard and reporting

## Project Structure

```
gopay/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and routes
│   ├── models.py            # Pydantic models
│   ├── supabase_util.py     # Supabase integration
│   ├── mpesa.py            # M-Pesa API integration
│   ├── qr_utils.py         # QR code generation
│   ├── templates/          # HTML templates
│   │   ├── pay.html
│   │   ├── driver_dashboard.html
│   │   └── admin_dashboard.html
│   └── static/
│       └── styles.css      # Custom styles
├── database/
│   ├── schema.sql          # PostgreSQL database schema
│   └── migrate.py          # Migration script
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
├── SUPABASE_SETUP.md      # Supabase setup guide
└── run.sh                # Startup script
```

## Database Schema

### PostgreSQL Tables

1. **drivers**
   ```sql
   CREATE TABLE drivers (
       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       name VARCHAR(255) NOT NULL,
       phone VARCHAR(20) NOT NULL UNIQUE,
       email VARCHAR(255) NOT NULL UNIQUE,
       vehicle_type vehicle_type NOT NULL,
       vehicle_number VARCHAR(50) NOT NULL,
       qr_code_url TEXT,
       balance DECIMAL(10,2) DEFAULT 0.00,
       total_earnings DECIMAL(10,2) DEFAULT 0.00,
       created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
       updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
   );
   ```

2. **transactions**
   ```sql
   CREATE TABLE transactions (
       id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
       driver_id UUID NOT NULL REFERENCES drivers(id),
       passenger_phone VARCHAR(20) NOT NULL,
       amount_paid DECIMAL(10,2) NOT NULL,
       platform_fee DECIMAL(10,2) NOT NULL,
       driver_amount DECIMAL(10,2) NOT NULL,
       status transaction_status DEFAULT 'pending',
       mpesa_receipt VARCHAR(100),
       checkout_request_id VARCHAR(100),
       created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
       updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
   );
   ```

3. **admin_stats**
   ```sql
   CREATE TABLE admin_stats (
       id VARCHAR(50) PRIMARY KEY DEFAULT 'revenue',
       total_transactions INTEGER DEFAULT 0,
       total_revenue DECIMAL(15,2) DEFAULT 0.00,
       total_platform_fees DECIMAL(15,2) DEFAULT 0.00,
       active_drivers INTEGER DEFAULT 0,
       updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
   );
   ```

## Setup Instructions

### Prerequisites

1. Python 3.8+
2. Supabase account
3. M-Pesa Daraja API account

### Supabase Setup

1. Create a new Supabase project at [supabase.com](https://supabase.com)
2. Get your project URL and API key from Settings → API
3. Run the database schema from `database/schema.sql` in the SQL Editor
4. Create a storage bucket named `qr-codes` and make it public

### M-Pesa Sandbox Setup

1. Create a Safaricom Developer Account
2. Create a new app to get your credentials
3. Configure your app settings
4. Note down your:
   - Consumer Key
   - Consumer Secret
   - Shortcode
   - Passkey

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mpesa-aggregator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `env.example` to `.env` and configure:
   ```bash
   cp env.example .env
   ```

5. Configure your environment variables in `.env`:
   ```
   # Supabase Configuration
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   
   # M-Pesa Configuration
   DARAJA_BASE_URL=https://sandbox.safaricom.co.ke
   DARAJA_CONSUMER_KEY=your-consumer-key
   DARAJA_CONSUMER_SECRET=your-consumer-secret
   DARAJA_SHORT_CODE=174379
   DARAJA_PASSKEY=your-passkey
   DARAJA_CALLBACK_URL=http://localhost:8000/api/mpesa/callback
   DARAJA_ACCOUNT_REF=GoPay
   DARAJA_TRANSACTION_DESC=Payment for ride
   ```

6. Run the application:
   ```bash
   ./run.sh
   ```

   The application will be available at `http://localhost:8000`

## Deployment

### Production Deployment Checklist

1. **Environment Configuration**
   - Set up production environment variables
   - Configure production Supabase project
   - Set up production M-Pesa credentials

2. **Security Measures**
   - Enable HTTPS
   - Set up CORS properly
   - Configure rate limiting
   - Implement request validation
   - Set up proper logging

3. **Performance Optimization**
   - Enable caching where appropriate
   - Optimize database queries
   - Configure proper connection pooling

### Deployment Options

1. **Docker Deployment**
   ```bash
   # Build the image
   docker build -t gopay-aggregator .
   
   # Run the container
   docker run -p 8000:8000 gopay-aggregator
   ```

2. **Cloud Platform Deployment**
   - Deploy to Google Cloud Run
   - Deploy to Heroku
   - Deploy to AWS ECS

## Security Checklist

- [x] Secure environment variables
- [x] Supabase Row Level Security (RLS)
- [x] Input validation
- [x] CORS configuration
- [x] Rate limiting
- [x] Error handling
- [x] Audit logging
- [x] Data encryption
- [x] Authentication
- [x] Authorization

## Troubleshooting

### Common Issues

1. **Supabase Connection Issues**
   - Verify SUPABASE_URL and SUPABASE_ANON_KEY
   - Check Supabase project settings
   - Verify environment variables

2. **M-Pesa API Issues**
   - Verify API credentials
   - Check callback URL configuration
   - Verify transaction parameters

3. **QR Code Generation Issues**
   - Check storage permissions
   - Verify Supabase Storage configuration
   - Check file upload settings

### Debug Mode

Enable debug mode by setting:
```python
app = FastAPI(debug=True)
```

### Logging

The application uses Python's built-in logging module. To enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the repository or contact the development team.







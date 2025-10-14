# GoPay Quick Start Guide

Get your GoPay application running in 5 minutes!

## Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
python setup_supabase.py
```

This interactive script will:
- Guide you through creating a Supabase account
- Help you configure environment variables
- Set up the database schema
- Install dependencies
- Test your connection

## Option 2: Manual Setup

### Step 1: Create Supabase Project (2 minutes)

1. Go to [supabase.com](https://supabase.com) and sign up
2. Click "New Project"
3. Name it "GoPay" and choose a region
4. Save your database password!
5. Wait for project creation (~2 minutes)

### Step 2: Get API Credentials (1 minute)

1. In Supabase dashboard: Settings → API
2. Copy:
   - **Project URL**
   - **anon public key**

### Step 3: Configure Environment (1 minute)

1. Copy the example file:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```env
   SUPABASE_URL=your_project_url_here
   SUPABASE_ANON_KEY=your_anon_key_here
   ```

### Step 4: Set Up Database (1 minute)

1. In Supabase dashboard: SQL Editor → New query
2. Copy all content from `database/schema.sql`
3. Paste and click "Run"
4. You should see "Success. No rows returned"

### Step 5: Create Storage Bucket (30 seconds)

1. In Supabase dashboard: Storage → Create bucket
2. Name: `qr-codes`
3. ✅ Check "Public bucket"
4. Click "Create"

### Step 6: Install & Run (30 seconds)

```bash
# Install dependencies
pip install -r requirements.txt

# Verify setup
python verify_setup.py

# Start the application
python -m uvicorn app.main:app --reload
```

## Verify Your Setup

Run the verification script to check everything:

```bash
python verify_setup.py
```

This will check:
- ✅ Environment variables
- ✅ Dependencies
- ✅ Supabase connection
- ✅ Database tables
- ✅ Storage bucket

## Start Your Application

```bash
python -m uvicorn app.main:app --reload
```

Or use the provided script:

```bash
# Linux/Mac
./run.sh

# Windows
python -m uvicorn app.main:app --reload
```

Visit: **http://localhost:8000**

## Test the API

Once running, visit:
- **API Documentation**: http://localhost:8000/docs
- **Admin Dashboard**: http://localhost:8000/admin/dashboard

## Next Steps

1. **Configure M-Pesa**: Update M-Pesa credentials in `.env`
2. **Register a Driver**: Use the `/api/register_driver` endpoint
3. **Test Payments**: Use the payment page with a driver ID
4. **Explore Dashboards**: Check driver and admin dashboards

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Connection refused" error
- Check your `SUPABASE_URL` and `SUPABASE_ANON_KEY` in `.env`
- Verify your internet connection

### "Table does not exist" error
- Make sure you ran `database/schema.sql` in Supabase SQL Editor
- Check for any errors in the SQL execution

### "Storage bucket not found" error
- Create `qr-codes` bucket in Supabase Storage
- Make sure it's set to public

## Need More Help?

- 📖 Full Setup Guide: `SUPABASE_SETUP.md`
- 🔍 Verification Tool: `python verify_setup.py`
- 📚 API Docs: http://localhost:8000/docs (when running)

## Common Commands

```bash
# Setup
python setup_supabase.py          # Interactive setup

# Verify
python verify_setup.py            # Check configuration

# Run
python -m uvicorn app.main:app --reload  # Start server

# Development
python -m uvicorn app.main:app --reload --port 8000  # Custom port

# Migration (if coming from Firebase)
python database/migrate.py        # Migrate data
```

Happy coding! 🚀

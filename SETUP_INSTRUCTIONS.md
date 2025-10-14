# Complete Supabase Setup Instructions for GoPay

Follow these steps to set up your GoPay application with Supabase.

## Prerequisites

- Python 3.8 or higher installed
- A web browser
- An email address
- 15 minutes of your time

---

## STEP 1: Create Supabase Account & Project

### 1.1 Sign Up for Supabase

1. Open your browser and go to: **https://supabase.com**
2. Click **"Start your project"** or **"Sign In"**
3. Sign up using one of these options:
   - GitHub account
   - Google account
   - Email address

### 1.2 Create New Project

1. Once logged in, click **"New Project"**
2. Select your organization (or create one)
3. Fill in the project details:
   
   ```
   Project Name: GoPay
   Database Password: [Choose a strong password - SAVE THIS!]
   Region: [Choose closest to your users]
     - East US (for US East Coast)
     - West US (for US West Coast)
     - Europe West (for Europe)
     - etc.
   Pricing Plan: Free
   ```

4. Click **"Create new project"**
5. **Wait 2-3 minutes** for the project to be created (grab a coffee! ☕)

---

## STEP 2: Get Your API Credentials

### 2.1 Navigate to API Settings

1. In your Supabase dashboard, look at the left sidebar
2. Click on **"Settings"** (gear icon at the bottom)
3. Click on **"API"** in the settings menu

### 2.2 Copy Your Credentials

You'll see two important values. **Copy and save both:**

**Project URL:**
```
https://xxxxxxxxxxxxx.supabase.co
```

**anon public key:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6...
(This is a long string)
```

💡 **TIP:** Keep this browser tab open - you'll need these values in the next step!

---

## STEP 3: Configure Environment Variables

### 3.1 Create .env File

1. Open your project folder in a text editor or IDE
2. Find the file named `env.example`
3. Copy it and rename the copy to `.env`

**Windows Command Prompt:**
```cmd
copy env.example .env
```

**PowerShell:**
```powershell
Copy-Item env.example .env
```

**Linux/Mac:**
```bash
cp env.example .env
```

### 3.2 Edit .env File

1. Open the `.env` file in a text editor
2. Replace the placeholder values with your actual credentials:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your_actual_anon_key_here

# M-Pesa Daraja API Configuration (update these later)
DARAJA_BASE_URL=https://sandbox.safaricom.co.ke
DARAJA_CONSUMER_KEY=your_consumer_key
DARAJA_CONSUMER_SECRET=your_consumer_secret
DARAJA_SHORT_CODE=174379
DARAJA_PASSKEY=your_passkey
DARAJA_CALLBACK_URL=http://localhost:8000/api/mpesa/callback
DARAJA_ACCOUNT_REF=GoPay
DARAJA_TRANSACTION_DESC=Payment for ride
```

3. **Save the file**

⚠️ **IMPORTANT:** The `.env` file contains sensitive information. Never commit it to Git!

---

## STEP 4: Set Up Database Schema

### 4.1 Open SQL Editor

1. Go back to your Supabase dashboard
2. Click on **"SQL Editor"** in the left sidebar
3. Click **"New query"** button

### 4.2 Run the Schema

1. Open the file `database/schema.sql` in your project folder
2. **Copy ALL the content** from that file (Ctrl+A, then Ctrl+C)
3. **Paste** it into the Supabase SQL Editor
4. Click **"Run"** button (or press Ctrl+Enter)

### 4.3 Verify Success

You should see a message like:
```
Success. No rows returned
```

This is good! It means all tables, functions, and indexes were created successfully.

💡 **What this does:**
- Creates `drivers` table
- Creates `transactions` table  
- Creates `admin_stats` table
- Sets up indexes for better performance
- Creates helper functions for atomic operations
- Sets up Row Level Security policies

---

## STEP 5: Create Storage Bucket for QR Codes

### 5.1 Navigate to Storage

1. In Supabase dashboard, click on **"Storage"** in the left sidebar
2. Click **"Create a new bucket"** button

### 5.2 Configure Bucket

Fill in the details:
```
Bucket name: qr-codes
Public bucket: ✅ (CHECK THIS BOX!)
File size limit: 50 MB (default is fine)
Allowed MIME types: image/png (or leave empty for all)
```

3. Click **"Create bucket"**

💡 **Why public?** QR codes need to be accessible to drivers and passengers without authentication.

---

## STEP 6: Install Python Dependencies

### 6.1 Open Terminal/Command Prompt

Navigate to your project directory:

```bash
cd path/to/GoPay
```

### 6.2 Install Packages

Run the following command:

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- Supabase (database client)
- Uvicorn (web server)
- QRCode (QR code generation)
- And other dependencies

⏱️ **This may take 1-2 minutes**

---

## STEP 7: Verify Your Setup

Run the verification script to check everything:

```bash
python verify_setup.py
```

This will check:
- ✅ Environment variables are configured
- ✅ All dependencies are installed
- ✅ Supabase connection works
- ✅ Database tables exist
- ✅ Storage bucket is accessible

### Expected Output:

```
======================================================================
  Verification Summary
======================================================================

✅ PASS     Environment Variables
✅ PASS     Python Dependencies
✅ PASS     Supabase Connection
✅ PASS     Database Tables
✅ PASS     Storage Bucket

Result: 5/5 checks passed

🎉 All checks passed! Your setup is complete!
```

---

## STEP 8: Start Your Application

### 8.1 Start the Server

Run:

```bash
python -m uvicorn app.main:app --reload
```

Or on Linux/Mac, you can use:

```bash
./run.sh
```

### 8.2 Verify It's Running

You should see output like:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 8.3 Open in Browser

Visit these URLs:

- **API Documentation:** http://localhost:8000/docs
- **Admin Dashboard:** http://localhost:8000/admin/dashboard
- **API Root:** http://localhost:8000

---

## STEP 9: Test the Application

### 9.1 Register a Test Driver

1. Go to http://localhost:8000/docs
2. Find the `POST /api/register_driver` endpoint
3. Click **"Try it out"**
4. Enter test data:

```json
{
  "name": "John Doe",
  "phone": "254712345678",
  "email": "john@example.com",
  "vehicle_type": "boda",
  "vehicle_number": "KAA123B"
}
```

5. Click **"Execute"**
6. You should get a response with a `driver_id` and `qr_code_url`

### 9.2 View Driver Dashboard

1. Copy the `driver_id` from the response
2. Visit: `http://localhost:8000/driver/{driver_id}/dashboard`
3. You should see the driver's dashboard with their QR code!

### 9.3 Check Admin Dashboard

Visit: http://localhost:8000/admin/dashboard

You should see:
- Total transactions: 0
- Total revenue: 0.00
- Active drivers: 1

---

## Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Connection refused" or "Invalid API key"

**Solution:**
1. Check your `.env` file
2. Verify `SUPABASE_URL` and `SUPABASE_ANON_KEY` are correct
3. Make sure there are no extra spaces or quotes
4. Restart your application

### Issue: "Table does not exist"

**Solution:**
1. Go to Supabase SQL Editor
2. Re-run the content from `database/schema.sql`
3. Check for any error messages in the SQL execution

### Issue: "Storage bucket not found"

**Solution:**
1. Go to Supabase Dashboard → Storage
2. Create bucket named `qr-codes`
3. Make sure "Public bucket" is checked

### Issue: Port 8000 already in use

**Solution:**
Use a different port:
```bash
python -m uvicorn app.main:app --reload --port 8001
```

---

## Next Steps

### 1. Configure M-Pesa (Optional)

If you want to test payments:

1. Sign up for Safaricom Daraja API: https://developer.safaricom.co.ke
2. Create a sandbox app
3. Get your credentials
4. Update the M-Pesa section in your `.env` file

### 2. Explore the API

Visit http://localhost:8000/docs to see all available endpoints:

- Register drivers
- Initiate payments
- View transactions
- Get statistics

### 3. Customize

- Modify templates in `app/templates/`
- Update styles in `app/static/styles.css`
- Add new features in `app/main.py`

---

## Useful Commands

```bash
# Start server
python -m uvicorn app.main:app --reload

# Start with custom port
python -m uvicorn app.main:app --reload --port 8001

# Verify setup
python verify_setup.py

# Run tests (if you add them)
pytest

# Check Python version
python --version

# List installed packages
pip list
```

---

## Getting Help

If you encounter issues:

1. **Check the verification script:** `python verify_setup.py`
2. **Review the logs:** Look at the terminal output for error messages
3. **Check Supabase Dashboard:** Look for errors in the Supabase logs
4. **Read the docs:** `SUPABASE_SETUP.md` has more detailed information

---

## Success Checklist

- [ ] Supabase project created
- [ ] API credentials copied
- [ ] `.env` file configured
- [ ] Database schema executed
- [ ] Storage bucket created
- [ ] Dependencies installed
- [ ] Verification script passed
- [ ] Application starts successfully
- [ ] Can access http://localhost:8000/docs
- [ ] Can register a test driver
- [ ] Can view dashboards

---

**Congratulations! Your GoPay application is now running on Supabase!** 🎉

For more information, check:
- `SUPABASE_SETUP.md` - Detailed setup guide
- `QUICKSTART.md` - Quick reference
- `README.md` - Project documentation

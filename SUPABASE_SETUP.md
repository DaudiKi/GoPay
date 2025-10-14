# Supabase Setup Guide for GoPay

This guide will help you set up Supabase for your GoPay payment aggregator project.

## Prerequisites

1. A Supabase account (sign up at [supabase.com](https://supabase.com))
2. Python 3.8+ installed
3. Your existing GoPay project

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign in
2. Click "New Project"
3. Choose your organization
4. Enter project details:
   - **Name**: GoPay
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Choose the closest region to your users
5. Click "Create new project"
6. Wait for the project to be created (2-3 minutes)

## Step 2: Get Your Supabase Credentials

1. In your Supabase dashboard, go to **Settings** → **API**
2. Copy the following values:
   - **Project URL** (SUPABASE_URL)
   - **anon public** key (SUPABASE_ANON_KEY)

## Step 3: Set Up Database Schema

1. In your Supabase dashboard, go to **SQL Editor**
2. Copy the contents of `database/schema.sql`
3. Paste it into the SQL editor
4. Click **Run** to execute the schema

This will create:
- `drivers` table
- `transactions` table  
- `admin_stats` table
- Required indexes and functions
- Storage bucket for QR codes

## Step 4: Configure Environment Variables

1. Copy `env.example` to `.env`:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` and add your Supabase credentials:
   ```env
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_ANON_KEY=your_anon_key_here
   ```

3. Add your M-Pesa credentials (keep existing values)

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 6: Test the Setup

1. Start your application:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

2. Test the API endpoints:
   - Register a driver: `POST /api/register_driver`
   - Get driver: `GET /api/driver/{driver_id}`
   - Admin dashboard: `GET /admin/dashboard`

## Step 7: Migrate Data (Optional)

If you have existing data in Firebase, you can migrate it:

1. Install Firebase admin (if not already installed):
   ```bash
   pip install firebase-admin
   ```

2. Set your Firebase credentials in `.env`:
   ```env
   GOOGLE_APPLICATION_CREDENTIALS=path/to/serviceAccount.json
   ```

3. Run the migration script:
   ```bash
   python database/migrate.py
   ```

## Step 8: Configure Storage (QR Codes)

1. In Supabase dashboard, go to **Storage**
2. You should see the `qr-codes` bucket created by the schema
3. If not, create it manually:
   - Click "New bucket"
   - Name: `qr-codes`
   - Make it public: ✅

## Step 9: Set Up Row Level Security (Optional)

For production, you should configure RLS policies:

1. Go to **Authentication** → **Policies**
2. Create policies for your tables based on your security requirements
3. The current setup allows all operations (for development)

## Troubleshooting

### Common Issues

1. **Connection Error**: Check your SUPABASE_URL and SUPABASE_ANON_KEY
2. **Schema Error**: Make sure you ran the complete schema.sql file
3. **Storage Error**: Ensure the `qr-codes` bucket exists and is public
4. **Migration Error**: Check your Firebase credentials path

### Getting Help

- Check the [Supabase Documentation](https://supabase.com/docs)
- Join the [Supabase Discord](https://discord.supabase.com)
- Check your project logs in the Supabase dashboard

## Next Steps

1. **Authentication**: Set up user authentication if needed
2. **Real-time**: Enable real-time subscriptions for live updates
3. **Backups**: Set up automated backups
4. **Monitoring**: Set up monitoring and alerts
5. **Security**: Review and tighten RLS policies

## Benefits of Supabase

✅ **PostgreSQL**: Full SQL support with ACID compliance  
✅ **Real-time**: Built-in real-time subscriptions  
✅ **Storage**: Integrated file storage  
✅ **Auth**: Built-in authentication system  
✅ **APIs**: Auto-generated REST and GraphQL APIs  
✅ **Dashboard**: Beautiful admin interface  
✅ **Open Source**: No vendor lock-in  

Your GoPay project is now running on Supabase! 🎉

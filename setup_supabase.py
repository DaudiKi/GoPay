#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Supabase Setup Script for GoPay
This script helps you set up your Supabase project interactively.
"""

import os
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_step(step_num, text):
    """Print a step number and description."""
    print(f"\n{'='*70}")
    print(f"STEP {step_num}: {text}")
    print('='*70 + "\n")

def wait_for_user():
    """Wait for user to press Enter."""
    input("\nPress Enter to continue...")

def main():
    print_header("🚀 GoPay Supabase Setup Assistant")
    
    print("""
This script will guide you through setting up Supabase for your GoPay project.
You'll need:
    - A web browser
    - An email address for Supabase account
    - 10-15 minutes
    """)
    
    wait_for_user()
    
    # Step 1: Create Supabase Account
    print_step(1, "Create Supabase Account & Project")
    print("""
1. Open your browser and go to: https://supabase.com
2. Click "Start your project" or "Sign In"
3. Sign up with GitHub, Google, or Email
4. Once logged in, click "New Project"
5. Fill in the project details:
   - Name: GoPay
   - Database Password: (Choose a strong password and SAVE IT!)
   - Region: Choose closest to your users (e.g., East US, Europe West)
   - Pricing Plan: Free (perfect for getting started)
6. Click "Create new project"
7. Wait 2-3 minutes for project creation...
    """)
    
    wait_for_user()
    
    # Step 2: Get API Credentials
    print_step(2, "Get Your API Credentials")
    print("""
1. In your Supabase dashboard, click on "Settings" (gear icon) in the left sidebar
2. Click on "API" in the settings menu
3. You'll see two important values:
   
   📋 Copy these values (you'll need them next):
   
   a) Project URL (looks like: https://xxxxxxxxxxxxx.supabase.co)
   b) anon public key (long string starting with "eyJ...")
   
4. Keep this tab open - we'll use these values next!
    """)
    
    wait_for_user()
    
    # Step 3: Configure Environment Variables
    print_step(3, "Configure Environment Variables")
    
    print("\nNow let's set up your environment variables...")
    print("\nPlease enter your Supabase credentials:\n")
    
    supabase_url = input("Enter your Supabase Project URL: ").strip()
    supabase_key = input("Enter your Supabase anon key: ").strip()
    
    if not supabase_url or not supabase_key:
        print("\n❌ Error: Both URL and key are required!")
        sys.exit(1)
    
    # Create .env file
    env_content = f"""# Supabase Configuration
SUPABASE_URL={supabase_url}
SUPABASE_ANON_KEY={supabase_key}

# M-Pesa Daraja API Configuration
DARAJA_BASE_URL=https://sandbox.safaricom.co.ke
DARAJA_CONSUMER_KEY=your_consumer_key
DARAJA_CONSUMER_SECRET=your_consumer_secret
DARAJA_SHORT_CODE=174379
DARAJA_PASSKEY=your_passkey
DARAJA_CALLBACK_URL=http://localhost:8000/api/mpesa/callback
DARAJA_ACCOUNT_REF=GoPay
DARAJA_TRANSACTION_DESC=Payment for ride
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ Environment variables saved to .env file!")
    print("\n⚠️  Remember to update your M-Pesa credentials later!")
    
    wait_for_user()
    
    # Step 4: Set up Database
    print_step(4, "Set Up Database Schema")
    print("""
Now let's create your database tables:

1. Go back to your Supabase dashboard
2. Click on "SQL Editor" in the left sidebar
3. Click "New query"
4. I'll open the schema file for you to copy...
    """)
    
    # Read and display schema
    schema_path = Path('database/schema.sql')
    if schema_path.exists():
        print(f"\n📄 Opening {schema_path}...")
        print("\n5. Copy ALL the content from 'database/schema.sql'")
        print("6. Paste it into the Supabase SQL Editor")
        print("7. Click 'Run' (or press Ctrl+Enter)")
        print("8. You should see 'Success. No rows returned' - that's good!")
        
        # Try to open the file
        try:
            if sys.platform == 'win32':
                os.system(f'notepad {schema_path}')
            elif sys.platform == 'darwin':
                os.system(f'open {schema_path}')
            else:
                os.system(f'xdg-open {schema_path}')
        except:
            print(f"\n💡 Manually open: {schema_path.absolute()}")
    else:
        print("\n❌ Error: schema.sql not found!")
        print("Please make sure you're running this from the project root directory.")
    
    wait_for_user()
    
    # Step 5: Set up Storage
    print_step(5, "Set Up Storage for QR Codes")
    print("""
Let's create a storage bucket for QR codes:

1. In Supabase dashboard, click on "Storage" in the left sidebar
2. Click "Create a new bucket"
3. Bucket name: qr-codes
4. ✅ Check "Public bucket" (so QR codes can be accessed)
5. Click "Create bucket"
6. Done! ✅
    """)
    
    wait_for_user()
    
    # Step 6: Install Dependencies
    print_step(6, "Install Python Dependencies")
    print("\nInstalling required packages...\n")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencies installed successfully!")
        else:
            print("⚠️  Some packages may have issues. Check the output above.")
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        print("\nPlease run manually: pip install -r requirements.txt")
    
    wait_for_user()
    
    # Step 7: Test Connection
    print_step(7, "Test Supabase Connection")
    print("\nLet's verify your Supabase connection...\n")
    
    try:
        from supabase import create_client
        
        supabase = create_client(supabase_url, supabase_key)
        
        # Try to query the drivers table
        result = supabase.table('drivers').select('count').execute()
        
        print("✅ Successfully connected to Supabase!")
        print("✅ Database tables are accessible!")
        
    except ImportError:
        print("⚠️  Supabase package not installed. Run: pip install supabase")
    except Exception as e:
        print(f"⚠️  Connection test failed: {e}")
        print("\nThis might be okay if you haven't run the schema yet.")
        print("Make sure you completed Step 4 (Database Schema).")
    
    wait_for_user()
    
    # Final Summary
    print_header("🎉 Setup Complete!")
    print("""
Your GoPay Supabase setup is complete! Here's what we did:

✅ Created Supabase project
✅ Configured environment variables (.env file)
✅ Set up database schema (tables, indexes, functions)
✅ Created storage bucket for QR codes
✅ Installed Python dependencies
✅ Tested connection

NEXT STEPS:
-----------
1. Update your M-Pesa credentials in the .env file
2. Start your application:
   
   python -m uvicorn app.main:app --reload
   
3. Open http://localhost:8000 in your browser
4. Test the API endpoints

USEFUL LINKS:
-------------
- Your Supabase Dashboard: https://app.supabase.com
- API Documentation: http://localhost:8000/docs (when app is running)
- Setup Guide: SUPABASE_SETUP.md

TROUBLESHOOTING:
----------------
If you encounter any issues:
1. Check your .env file has correct credentials
2. Verify database schema was run successfully
3. Ensure storage bucket 'qr-codes' exists and is public
4. Check Supabase dashboard for any errors

Need help? Check SUPABASE_SETUP.md for detailed instructions.

Happy coding! 🚀
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ An error occurred: {e}")
        sys.exit(1)

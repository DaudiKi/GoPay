#!/usr/bin/env python3
"""
Verify Supabase Setup for GoPay
This script checks if your Supabase setup is correct.
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables."""
    print("Checking environment variables...")
    
    if not Path('.env').exists():
        print("❌ .env file not found!")
        print("   Run: python setup_supabase.py")
        return False
    
    required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY']
    missing_vars = []
    
    from dotenv import load_dotenv
    load_dotenv()
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ Environment variables configured")
    return True

def check_supabase_connection():
    """Check if we can connect to Supabase."""
    print("\nTesting Supabase connection...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from supabase import create_client
        
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        supabase = create_client(supabase_url, supabase_key)
        
        # Try to access the drivers table
        result = supabase.table('drivers').select('*').limit(1).execute()
        
        print("✅ Successfully connected to Supabase")
        print("✅ Database is accessible")
        return True
        
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("   Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nPossible issues:")
        print("   - Check your SUPABASE_URL and SUPABASE_ANON_KEY")
        print("   - Make sure you ran the database schema (database/schema.sql)")
        print("   - Check your internet connection")
        return False

def check_database_tables():
    """Check if all required tables exist."""
    print("\nChecking database tables...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from supabase import create_client
        
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        supabase = create_client(supabase_url, supabase_key)
        
        tables = ['drivers', 'transactions', 'admin_stats']
        all_exist = True
        
        for table in tables:
            try:
                supabase.table(table).select('*').limit(1).execute()
                print(f"   ✅ Table '{table}' exists")
            except Exception as e:
                print(f"   ❌ Table '{table}' not found")
                all_exist = False
        
        if all_exist:
            print("\n✅ All database tables exist")
            return True
        else:
            print("\n❌ Some tables are missing")
            print("   Run the schema: database/schema.sql in Supabase SQL Editor")
            return False
            
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def check_storage_bucket():
    """Check if storage bucket exists."""
    print("\nChecking storage bucket...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from supabase import create_client
        
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        supabase = create_client(supabase_url, supabase_key)
        
        # Try to list buckets
        buckets = supabase.storage.list_buckets()
        
        qr_bucket_exists = any(b.name == 'qr-codes' for b in buckets)
        
        if qr_bucket_exists:
            print("✅ Storage bucket 'qr-codes' exists")
            return True
        else:
            print("❌ Storage bucket 'qr-codes' not found")
            print("   Create it in Supabase Dashboard → Storage → New bucket")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not verify storage bucket: {e}")
        print("   (This is optional, but needed for QR codes)")
        return False

def check_dependencies():
    """Check if all required packages are installed."""
    print("\nChecking Python dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'supabase',
        'qrcode',
        'requests',
        'jinja2',
        'pydantic',
        'python-dotenv'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed")
    return True

def main():
    print("="*70)
    print("  🔍 GoPay Supabase Setup Verification")
    print("="*70)
    print()
    
    checks = [
        ("Environment Variables", check_env_file),
        ("Python Dependencies", check_dependencies),
        ("Supabase Connection", check_supabase_connection),
        ("Database Tables", check_database_tables),
        ("Storage Bucket", check_storage_bucket),
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error during {name} check: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("="*70)
    print("  📊 VERIFICATION SUMMARY")
    print("="*70)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} {name}")
    
    print()
    print(f"Result: {passed}/{total} checks passed")
    print()
    
    if passed == total:
        print("🎉 All checks passed! Your setup is complete!")
        print()
        print("You can now start your application:")
        print("   python -m uvicorn app.main:app --reload")
        print()
        print("Then visit: http://localhost:8000")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print()
        print("Need help? Check SUPABASE_SETUP.md for detailed instructions.")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nVerification cancelled.")
        sys.exit(1)

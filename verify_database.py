"""
Verify Database Migration Status
Checks if IntaSend tables and columns exist in Supabase
"""
import os
from dotenv import load_dotenv
from supabase import create_client

def verify_database():
    """Check if database has required IntaSend tables and columns."""
    
    # Load environment
    if os.path.exists('.env.production'):
        load_dotenv('.env.production')
        print("📋 Using: .env.production")
    elif os.path.exists('.env'):
        load_dotenv()
        print("📋 Using: .env")
    else:
        print("❌ No .env file found!")
        return False
    
    # Get Supabase credentials
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Supabase credentials not found!")
        print("   Set SUPABASE_URL and SUPABASE_ANON_KEY")
        return False
    
    print(f"🔗 Connecting to: {supabase_url}")
    
    try:
        # Create Supabase client
        supabase = create_client(supabase_url, supabase_key)
        
        print("\n" + "="*60)
        print("Checking Database Schema...")
        print("="*60)
        
        # Check 1: Payouts table
        print("\n1️⃣  Checking: payouts table")
        try:
            result = supabase.table('payouts').select('*').limit(1).execute()
            print("   ✅ Table exists: payouts")
        except Exception as e:
            print(f"   ❌ Table missing: payouts")
            print(f"      Error: {str(e)}")
            return False
        
        # Check 2: Platform fees table
        print("\n2️⃣  Checking: platform_fees table")
        try:
            result = supabase.table('platform_fees').select('*').limit(1).execute()
            print("   ✅ Table exists: platform_fees")
        except Exception as e:
            print(f"   ❌ Table missing: platform_fees")
            print(f"      Error: {str(e)}")
            return False
        
        # Check 3: Transactions table with IntaSend columns
        print("\n3️⃣  Checking: transactions table (IntaSend columns)")
        try:
            # Try to select IntaSend-specific columns
            result = supabase.table('transactions').select(
                'id, intasend_collection_id, intasend_tracking_id, '
                'collection_status, payout_status'
            ).limit(1).execute()
            print("   ✅ IntaSend columns exist in transactions table")
        except Exception as e:
            print(f"   ❌ IntaSend columns missing in transactions table")
            print(f"      Error: {str(e)}")
            return False
        
        # Check 4: Drivers table exists
        print("\n4️⃣  Checking: drivers table")
        try:
            result = supabase.table('drivers').select('id, name').limit(1).execute()
            print("   ✅ Table exists: drivers")
            
            # Show count
            count_result = supabase.table('drivers').select('id', count='exact').execute()
            driver_count = len(count_result.data) if count_result.data else 0
            print(f"   📊 Current drivers: {driver_count}")
        except Exception as e:
            print(f"   ❌ Table missing: drivers")
            print(f"      Error: {str(e)}")
            return False
        
        # Check 5: Test basic operations
        print("\n5️⃣  Testing: Database operations")
        try:
            # Test reading from multiple tables
            supabase.table('drivers').select('*').limit(1).execute()
            supabase.table('transactions').select('*').limit(1).execute()
            supabase.table('payouts').select('*').limit(1).execute()
            supabase.table('platform_fees').select('*').limit(1).execute()
            print("   ✅ All tables accessible")
        except Exception as e:
            print(f"   ❌ Database operation failed: {str(e)}")
            return False
        
        # Get statistics
        print("\n" + "="*60)
        print("Database Statistics")
        print("="*60)
        
        try:
            # Count records
            transactions = supabase.table('transactions').select('id', count='exact').execute()
            payouts = supabase.table('payouts').select('id', count='exact').execute()
            fees = supabase.table('platform_fees').select('id', count='exact').execute()
            
            trans_count = len(transactions.data) if transactions.data else 0
            payout_count = len(payouts.data) if payouts.data else 0
            fee_count = len(fees.data) if fees.data else 0
            
            print(f"\n📊 Drivers: {driver_count}")
            print(f"📊 Transactions: {trans_count}")
            print(f"📊 Payouts: {payout_count}")
            print(f"📊 Platform Fees: {fee_count}")
        except Exception as e:
            print(f"⚠️  Could not get statistics: {str(e)}")
        
        print("\n" + "="*60)
        print("✅ Database Verification Passed!")
        print("="*60)
        print("\n✅ Your database is ready for IntaSend integration!")
        print("   All required tables and columns are present.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check SUPABASE_URL is correct")
        print("2. Check SUPABASE_ANON_KEY is correct")
        print("3. Verify your Supabase project is active")
        return False


def print_migration_instructions():
    """Print instructions for running migration if needed."""
    print("\n" + "="*60)
    print("Migration Required")
    print("="*60)
    print("\nYour database needs to be updated for IntaSend.")
    print("\n📝 Steps to migrate:")
    print("\n1. Go to your Supabase project: https://app.supabase.com")
    print("2. Navigate to: SQL Editor")
    print("3. Click: New Query")
    print("4. Copy contents of: database/intasend_migration.sql")
    print("5. Paste into SQL Editor")
    print("6. Click: Run")
    print("\n7. After running, execute this script again to verify")
    print("\nMigration file: database/intasend_migration.sql")
    print("="*60)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  GoPay Database Verification")
    print("="*60 + "\n")
    
    success = verify_database()
    
    if not success:
        print_migration_instructions()
        exit(1)
    else:
        print("\n✅ Verification completed successfully!")
        print("   You're ready to proceed with production deployment.")
        exit(0)


#!/usr/bin/env python3
"""
IntaSend Setup Verification Script
This script verifies that your IntaSend integration is properly configured
"""

import os
import sys
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    print(f"{BLUE}ℹ {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠ {message}{RESET}")

def print_header(message):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{message:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def verify_environment_variables():
    """Verify all required environment variables are set"""
    print_header("Checking Environment Variables")
    
    all_good = True
    required_vars = {
        'SUPABASE_URL': 'https://your-project.supabase.co',
        'SUPABASE_ANON_KEY': 'your-supabase-anon-key-here',
        'INTASEND_API_KEY': 'your-intasend-secret-api-key-here',
        'INTASEND_PUBLISHABLE_KEY': 'ISPubKey_',
        'INTASEND_TEST_MODE': None,
        'PLATFORM_FEE_PERCENTAGE': None,
        'PLATFORM_FEE_FIXED': None,
        'BASE_PUBLIC_URL': None
    }
    
    for var, invalid_value in required_vars.items():
        value = os.getenv(var)
        
        if not value:
            print_error(f"{var} is not set")
            all_good = False
        elif invalid_value and value == invalid_value:
            print_error(f"{var} is set to default/invalid value")
            all_good = False
        elif invalid_value and invalid_value.startswith('ISPubKey_') and not value.startswith('ISPubKey_'):
            print_error(f"{var} does not start with 'ISPubKey_'")
            all_good = False
        else:
            # Don't print the full value for security
            masked_value = value[:15] + '...' if len(value) > 15 else value
            print_success(f"{var} = {masked_value}")
    
    return all_good

def verify_intasend_connection():
    """Test connection to IntaSend API"""
    print_header("Testing IntaSend API Connection")
    
    try:
        from app.intasend import IntaSendAPI
        
        api = IntaSendAPI()
        print_success("IntaSend API client initialized")
        
        # Check configuration
        if api.is_test:
            print_warning("Running in SANDBOX/TEST mode")
            print_info("Use sandbox test numbers: 254722000000, 254722000001")
        else:
            print_warning("Running in PRODUCTION mode")
            print_info("Real money will be charged!")
        
        print_success(f"Base URL: {api.base_url}")
        
        # Test fee calculation
        test_amount = 100
        fees = api.calculate_fees(test_amount)
        print_success("Fee calculation working:")
        print(f"  Amount: {fees['total_amount']} KES")
        print(f"  Platform Fee: {fees['platform_fee']} KES ({fees['fee_percentage']}%)")
        print(f"  Driver Amount: {fees['driver_amount']} KES")
        
        return True
    except ImportError as e:
        print_error(f"Failed to import IntaSend API: {e}")
        print_info("Make sure dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print_error(f"IntaSend initialization failed: {e}")
        return False

def verify_supabase_connection():
    """Test connection to Supabase"""
    print_header("Testing Supabase Connection")
    
    try:
        from app.supabase_util import SupabaseManager
        
        manager = SupabaseManager()
        print_success("Supabase client initialized")
        
        # Try to query a table (just to verify connection)
        try:
            result = manager.supabase.table('drivers').select('count', count='exact').limit(0).execute()
            print_success(f"Connected to Supabase successfully")
            print_info(f"Database has {result.count if hasattr(result, 'count') else 'unknown'} drivers")
        except Exception as e:
            print_warning(f"Could not query drivers table: {e}")
            print_info("This is normal if you haven't registered any drivers yet")
        
        return True
    except ImportError as e:
        print_error(f"Failed to import Supabase utilities: {e}")
        return False
    except Exception as e:
        print_error(f"Supabase initialization failed: {e}")
        print_info("Check your SUPABASE_URL and SUPABASE_ANON_KEY")
        return False

def verify_database_schema():
    """Verify that required database tables exist"""
    print_header("Verifying Database Schema")
    
    try:
        from app.supabase_util import SupabaseManager
        
        manager = SupabaseManager()
        
        required_tables = ['drivers', 'transactions', 'payouts', 'platform_fees']
        
        for table in required_tables:
            try:
                result = manager.supabase.table(table).select('count', count='exact').limit(0).execute()
                print_success(f"Table '{table}' exists")
            except Exception as e:
                print_error(f"Table '{table}' not found or error: {e}")
                print_info(f"Run database/intasend_migration.sql in Supabase SQL Editor")
                return False
        
        return True
    except Exception as e:
        print_error(f"Database schema verification failed: {e}")
        return False

def verify_file_structure():
    """Verify that all required files exist"""
    print_header("Verifying File Structure")
    
    required_files = [
        'app/intasend.py',
        'app/main_intasend.py',
        'app/models.py',
        'app/supabase_util.py',
        'app/qr_utils.py',
        'database/intasend_migration.sql',
        'requirements.txt',
        '.env'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print_success(f"{file_path} exists")
        else:
            print_error(f"{file_path} NOT FOUND")
            all_exist = False
    
    return all_exist

def verify_dependencies():
    """Verify that required Python packages are installed"""
    print_header("Verifying Python Dependencies")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'supabase',
        'pydantic',
        'python-dotenv',
        'requests',
        'qrcode'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print_success(f"{package} is installed")
        except ImportError:
            print_error(f"{package} is NOT installed")
            all_installed = False
    
    if not all_installed:
        print_info("Install missing packages: pip install -r requirements.txt")
    
    return all_installed

async def test_intasend_api():
    """Test actual IntaSend API calls (optional)"""
    print_header("Testing IntaSend API Calls (Optional)")
    
    response = input("Do you want to test actual API calls to IntaSend? (y/n): ")
    if response.lower() != 'y':
        print_info("Skipping API call tests")
        return True
    
    try:
        from app.intasend import IntaSendAPI
        
        api = IntaSendAPI()
        
        # Test wallet balance
        print_info("Testing wallet balance check...")
        try:
            balance = await api.get_wallet_balance()
            print_success("Wallet balance retrieved successfully")
            if isinstance(balance, dict) and 'wallets' in balance:
                for wallet in balance['wallets']:
                    currency = wallet.get('currency', 'KES')
                    available = wallet.get('available_balance', 0)
                    print(f"  {currency} Balance: {available}")
            else:
                print_info(f"Balance response: {balance}")
        except Exception as e:
            print_error(f"Failed to get wallet balance: {e}")
            print_info("This might be a permissions issue or API key problem")
            return False
        
        return True
    except Exception as e:
        print_error(f"API test failed: {e}")
        return False

def print_summary(checks):
    """Print summary of all checks"""
    print_header("Summary")
    
    total = len(checks)
    passed = sum(checks.values())
    failed = total - passed
    
    if failed == 0:
        print_success(f"All {total} checks passed! ✨")
        print()
        print_info("You're ready to start the application:")
        print("  uvicorn app.main_intasend:app --reload --host 0.0.0.0 --port 8000")
        print()
        print_info("Next steps:")
        print("  1. Register a test driver")
        print("  2. Test payment flow")
        print("  3. Verify webhook handling")
        print("  4. Check database records")
    else:
        print_error(f"{failed} check(s) failed out of {total}")
        print_warning("Please fix the issues above before starting the application")
    
    print()
    print("Detailed results:")
    for check_name, passed in checks.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        color = GREEN if passed else RED
        print(f"  {color}{status}{RESET} - {check_name}")

def main():
    """Main verification function"""
    print()
    print("="*60)
    print(" GoPay with IntaSend - Setup Verification".center(60))
    print("="*60)
    print()
    
    checks = {}
    
    # Run all checks
    checks['File Structure'] = verify_file_structure()
    checks['Environment Variables'] = verify_environment_variables()
    checks['Python Dependencies'] = verify_dependencies()
    checks['Supabase Connection'] = verify_supabase_connection()
    checks['Database Schema'] = verify_database_schema()
    checks['IntaSend API'] = verify_intasend_connection()
    
    # Optional API test
    if checks['IntaSend API']:
        try:
            checks['IntaSend API Calls'] = asyncio.run(test_intasend_api())
        except Exception as e:
            print_error(f"API call test failed: {e}")
            checks['IntaSend API Calls'] = False
    
    # Print summary
    print_summary(checks)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nVerification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


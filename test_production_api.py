"""
Test IntaSend Production API Connection
Run this script to verify your production API keys work correctly.
"""
import os
import sys
from dotenv import load_dotenv
import requests

def test_production_api():
    """Test IntaSend production API connection."""
    
    # Try to load .env.production first, fall back to .env
    if os.path.exists('.env.production'):
        load_dotenv('.env.production')
        print("📋 Loaded configuration from: .env.production")
    else:
        load_dotenv()
        print("📋 Loaded configuration from: .env")
    
    # Get configuration
    api_key = os.getenv('INTASEND_API_KEY')
    pub_key = os.getenv('INTASEND_PUBLISHABLE_KEY')
    test_mode = os.getenv('INTASEND_TEST_MODE', 'true').lower() == 'true'
    
    if not api_key or not pub_key:
        print("❌ Error: API keys not found in environment!")
        print("   Make sure INTASEND_API_KEY and INTASEND_PUBLISHABLE_KEY are set")
        return False
    
    # Determine environment
    if test_mode:
        base_url = "https://sandbox.intasend.com/api/v1"
        env_name = "SANDBOX"
        print(f"⚠️  Warning: Running in SANDBOX mode (test mode = true)")
    else:
        base_url = "https://payment.intasend.com/api/v1"
        env_name = "PRODUCTION"
        print(f"🚀 Running in PRODUCTION mode (test mode = false)")
    
    # Validate key format
    key_prefix = api_key[:20] if len(api_key) > 20 else api_key
    pub_prefix = pub_key[:20] if len(pub_key) > 20 else pub_key
    
    print(f"\n🔑 API Key: {key_prefix}...")
    print(f"🔑 Publishable Key: {pub_prefix}...")
    print(f"🌍 Environment: {env_name}")
    print(f"🔗 Base URL: {base_url}")
    
    # Check if using correct keys for environment
    if test_mode and not api_key.startswith('ISSecretKey_test'):
        print("\n⚠️  WARNING: You're in test mode but API key doesn't look like sandbox key!")
        print("   Sandbox keys start with: ISSecretKey_test_")
    elif not test_mode and not api_key.startswith('ISSecretKey_live'):
        print("\n⚠️  WARNING: You're in production mode but API key doesn't look like production key!")
        print("   Production keys start with: ISSecretKey_live_")
    
    # Prepare request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("\n" + "="*60)
    print("Testing API Connection...")
    print("="*60)
    
    try:
        # Test 1: Get wallet balance
        print("\n1️⃣  Testing: Get Wallet Balance")
        response = requests.get(f"{base_url}/wallets/", headers=headers, timeout=10)
        
        if response.status_code == 200:
            wallet_data = response.json()
            print("   ✅ API Connection Successful!")
            
            # Handle both single wallet and multiple wallets response
            if isinstance(wallet_data, list) and len(wallet_data) > 0:
                wallet = wallet_data[0]
            elif isinstance(wallet_data, dict):
                wallet = wallet_data
            else:
                print(f"   ⚠️  Unexpected response format: {wallet_data}")
                return False
            
            currency = wallet.get('currency', 'KES')
            balance = wallet.get('available_balance', wallet.get('balance', '0.00'))
            
            print(f"   💰 Wallet Balance: {balance} {currency}")
            
            # Warn if balance is low in production
            if not test_mode:
                try:
                    balance_float = float(balance)
                    if balance_float < 1000:
                        print(f"   ⚠️  LOW BALANCE WARNING: {balance} {currency}")
                        print("      Consider adding funds for payouts")
                    elif balance_float == 0:
                        print(f"   ❌ ZERO BALANCE: Please fund your wallet before processing payouts!")
                except ValueError:
                    pass
            
        elif response.status_code == 401:
            print("   ❌ Authentication Failed!")
            print("   Error: Invalid API key")
            print(f"   Response: {response.text}")
            return False
        else:
            print(f"   ❌ Request Failed!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Test 2: Check collections service
        print("\n2️⃣  Testing: Collections Service")
        # Try to list recent collections
        response = requests.get(f"{base_url}/payment/collection/", headers=headers, timeout=10)
        
        if response.status_code in [200, 404]:  # 404 is ok if no collections yet
            print("   ✅ Collections Service: Accessible")
        else:
            print(f"   ⚠️  Collections Service: Status {response.status_code}")
        
        # Test 3: Check payouts service
        print("\n3️⃣  Testing: Payouts Service")
        response = requests.get(f"{base_url}/payouts/", headers=headers, timeout=10)
        
        if response.status_code in [200, 404]:  # 404 is ok if no payouts yet
            print("   ✅ Payouts Service: Accessible")
            
            # Check if payouts are enabled
            if not test_mode:
                print("   ℹ️  Make sure payouts are enabled in dashboard:")
                print("      → Dashboard → Payouts → Enable M-Pesa Disbursements")
                print("      → Set approval to: 'No approval required'")
        else:
            print(f"   ⚠️  Payouts Service: Status {response.status_code}")
        
        print("\n" + "="*60)
        print("✅ All Tests Passed!")
        print("="*60)
        
        if not test_mode:
            print("\n🎯 Production Checklist:")
            print("   □ Webhook configured in IntaSend dashboard")
            print("   □ Wallet funded (sufficient for payouts)")
            print("   □ Collections enabled")
            print("   □ Payouts enabled (no approval required)")
            print("   □ SSL/HTTPS configured on domain")
            print("\n   Ready to process real payments! 🚀")
        else:
            print("\n🧪 Sandbox Mode Active")
            print("   You can test without real money.")
            print("   Switch to production when ready:")
            print("   1. Get production keys from dashboard")
            print("   2. Set INTASEND_TEST_MODE=false")
            print("   3. Run this test again")
        
        return True
        
    except requests.exceptions.Timeout:
        print("   ❌ Request Timeout!")
        print("   Check your internet connection")
        return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection Error!")
        print("   Check your internet connection")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  IntaSend Production API Test")
    print("="*60 + "\n")
    
    success = test_production_api()
    
    if not success:
        print("\n❌ Test Failed!")
        print("\nTroubleshooting:")
        print("1. Check your API keys in .env or .env.production")
        print("2. Verify keys are from correct environment (sandbox vs production)")
        print("3. Make sure you have internet connection")
        print("4. Check IntaSend dashboard for service status")
        sys.exit(1)
    else:
        print("\n✅ Connection test completed successfully!")
        sys.exit(0)


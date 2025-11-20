#!/usr/bin/env python3
"""Create a test driver with phone number in QR code"""

import os
import random
import requests
from dotenv import load_dotenv
load_dotenv()

# Generate random data
random_num = random.randint(100, 999)
passenger_phone = f"254722{random_num}456"  # This will be pre-filled
data = {
    'name': f'Test Driver {random_num}',
    'phone': f'254700{random_num}123',  # Driver's phone
    'email': f'driver{random_num}@gopay.com',
    'vehicle_type': 'boda',
    'vehicle_number': f'KBW {random_num}B'
}

print("=" * 70)
print("CREATING TEST DRIVER WITH PHONE PRE-FILL")
print("=" * 70)

print("\nRegistering driver...")
response = requests.post('http://localhost:8000/api/register_driver', json=data)
result = response.json()

if 'driver_id' in result:
    driver_id = result['driver_id']
    base_url = os.getenv('BASE_PUBLIC_URL', 'http://localhost:8000').rstrip('/')
    
    print("\n[SUCCESS] Driver created!")
    print(f"\nDriver Details:")
    print(f"  Name: {data['name']}")
    print(f"  Phone: {data['phone']}")
    print(f"  Vehicle: {data['vehicle_type'].upper()} {data['vehicle_number']}")
    
    print(f"\nPassenger Phone (will be pre-filled):")
    print(f"  {passenger_phone}")
    
    print(f"\nURLs (should work on your phone):")
    print(f"\n1. Driver Dashboard:")
    print(f"   {base_url}/driver/{driver_id}/dashboard")
    
    print(f"\n2. Payment URL with pre-filled phone:")
    print(f"   {base_url}/pay?driver_id={driver_id}&phone={passenger_phone}")
    
    print("\nTo test:")
    print("1. Open the Driver Dashboard URL on your computer")
    print("2. Find the QR code on the dashboard")
    print("3. Scan it with your phone")
    print("4. The payment page should open with your phone number pre-filled!")
    print("5. You only need to enter the amount")
else:
    print("\n[ERROR] Failed to create driver:")
    print(result)

print("\n" + "=" * 70)

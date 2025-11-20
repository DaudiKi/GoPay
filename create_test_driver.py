#!/usr/bin/env python3
"""Create a test driver with proper QR code"""

import os
import random
import requests
from dotenv import load_dotenv
load_dotenv()

# Generate random data
random_num = random.randint(10000000, 99999999)
data = {
    'name': f'Test Driver {random_num}',
    'phone': f'2547{random_num}',
    'email': f'driver{random_num}@gopay.com',
    'vehicle_type': 'boda',
    'vehicle_number': f'KAA{random_num}T'
}

print("=" * 70)
print("CREATING TEST DRIVER")
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
    print(f"  Vehicle: {data['vehicle_type']} - {data['vehicle_number']}")
    
    print(f"\nURLs (should work on your phone):")
    print(f"\n1. Driver Dashboard:")
    print(f"   {base_url}/driver/{driver_id}/dashboard")
    
    print(f"\n2. Payment URL:")
    print(f"   {base_url}/pay?driver_id={driver_id}")
    
    print(f"\n3. Payment URL with phone:")
    print(f"   {base_url}/pay?driver_id={driver_id}&phone={data['phone']}")
    
    print(f"\n4. QR Code URL:")
    print(f"   {result.get('qr_code_url')}")
    
    print("\nTo test:")
    print("1. Open the Driver Dashboard URL on your computer")
    print("2. Find the QR code on the dashboard")
    print("3. Scan it with your phone")
    print("4. It should open the payment page!")
else:
    print("\n[ERROR] Failed to create driver:")
    print(result)

print("\n" + "=" * 70)

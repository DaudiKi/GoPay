#!/usr/bin/env python3
"""Create a test driver with better formatting"""

import os
import random
import requests
from dotenv import load_dotenv
load_dotenv()

# Generate random data
random_num = random.randint(100, 999)
data = {
    'name': f'John Doe',
    'phone': f'254722{random_num}123',
    'email': f'john{random_num}@gopay.com',
    'vehicle_type': 'boda',  # This will be properly formatted
    'vehicle_number': f'KBW {random_num}B'  # Added space for better readability
}

print("=" * 70)
print("CREATING TEST DRIVER WITH BETTER FORMATTING")
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
    
    print(f"\nURLs (should work on your phone):")
    print(f"\n1. Driver Dashboard:")
    print(f"   {base_url}/driver/{driver_id}/dashboard")
    
    print(f"\n2. Payment URL:")
    print(f"   {base_url}/pay?driver_id={driver_id}")
    
    print(f"\n3. Payment URL with phone:")
    print(f"   {base_url}/pay?driver_id={driver_id}&phone={data['phone']}")
    
    print("\nTo test:")
    print("1. Open the Driver Dashboard URL on your computer")
    print("2. Find the QR code on the dashboard")
    print("3. Scan it with your phone")
    print("4. The payment page should open with better formatting!")
else:
    print("\n[ERROR] Failed to create driver:")
    print(result)

print("\n" + "=" * 70)

#!/usr/bin/env python3
"""Create a test driver with M-Pesa payment QR code"""

import os
import random
import requests
from dotenv import load_dotenv
load_dotenv()

# Generate random data
random_num = random.randint(100, 999)
data = {
    'name': f'Test Driver {random_num}',
    'phone': f'254700{random_num}123',  # Driver's phone
    'email': f'driver{random_num}@gopay.com',
    'vehicle_type': 'boda',
    'vehicle_number': f'KBW {random_num}B'
}

print("=" * 70)
print("CREATING M-PESA PAYMENT QR CODE")
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
    print(f"  Vehicle: {data['vehicle_type'].upper()} {data['vehicle_number']}")
    
    print(f"\nPayment Process:")
    print("1. Scan QR code with your phone")
    print("2. Enter amount to pay")
    print("3. Click Pay Now")
    print("4. Enter M-Pesa PIN when prompted")
    
    print(f"\nURLs (scan with your phone):")
    print(f"\n1. Driver Dashboard:")
    print(f"   {base_url}/driver/{driver_id}/dashboard")
    
    print(f"\n2. Direct Payment Link:")
    print(f"   {base_url}/pay?driver_id={driver_id}&phone=254722000000")
    print("   (Replace 254722000000 with your actual M-Pesa number)")
else:
    print("\n[ERROR] Failed to create driver:")
    print(result)

print("\n" + "=" * 70)

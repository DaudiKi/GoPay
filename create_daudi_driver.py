#!/usr/bin/env python3
"""Create driver account for Daudi"""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

# Driver data
data = {
    'name': 'Daudi Makumbi',
    'phone': '254740915456',  # Formatted without + for M-Pesa
    'email': 'daudimakumbik@gmail.com',
    'vehicle_type': 'boda',
    'vehicle_number': 'KDK 102A'
}

print("=" * 70)
print("CREATING DRIVER ACCOUNT")
print("=" * 70)

print("\nRegistering driver...")
response = requests.post('http://localhost:8000/api/register_driver', json=data)
result = response.json()

if 'driver_id' in result:
    driver_id = result['driver_id']
    base_url = os.getenv('BASE_PUBLIC_URL', 'http://localhost:8000').rstrip('/')
    
    print("\n[SUCCESS] Driver account created!")
    print(f"\nDriver Details:")
    print(f"  Name: {data['name']}")
    print(f"  Phone: {data['phone']}")
    print(f"  Email: {data['email']}")
    print(f"  Vehicle: {data['vehicle_type'].upper()} {data['vehicle_number']}")
    
    print(f"\nDashboard & Payment Links:")
    print(f"\n1. Driver Dashboard (open on computer):")
    print(f"   {base_url}/driver/{driver_id}/dashboard")
    
    print(f"\n2. Payment Link (for passengers):")
    print(f"   {base_url}/pay?driver_id={driver_id}&phone=254740915456")
    
    print("\nTo receive payments:")
    print("1. Open your dashboard")
    print("2. Show the QR code to passenger")
    print("3. They scan and enter amount")
    print("4. You'll get M-Pesa prompt on +254740915456")
else:
    print("\n[ERROR] Failed to create driver:")
    print(result)

print("\n" + "=" * 70)

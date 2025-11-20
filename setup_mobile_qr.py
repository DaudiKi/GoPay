#!/usr/bin/env python3
"""Setup mobile-friendly QR codes"""

import os
import socket
import requests
from dotenv import load_dotenv
load_dotenv()

def get_local_ip():
    """Get the local IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def update_env_file():
    """Update .env file with BASE_PUBLIC_URL"""
    ip = get_local_ip()
    base_url = f"http://{ip}:8000"
    
    # Read current .env content
    env_content = ""
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
    except FileNotFoundError:
        env_content = ""
    
    # Check if BASE_PUBLIC_URL exists
    if 'BASE_PUBLIC_URL=' in env_content:
        # Update existing value
        lines = env_content.splitlines()
        new_lines = []
        for line in lines:
            if line.startswith('BASE_PUBLIC_URL='):
                new_lines.append(f'BASE_PUBLIC_URL={base_url}')
            else:
                new_lines.append(line)
        new_content = '\n'.join(new_lines)
    else:
        # Add new value at the top
        new_content = f'BASE_PUBLIC_URL={base_url}\n{env_content}'
    
    # Write back to .env
    with open('.env', 'w') as f:
        f.write(new_content)
    
    return base_url

if __name__ == '__main__':
    print("=" * 70)
    print("SETTING UP MOBILE-FRIENDLY QR CODES")
    print("=" * 70)
    
    # Update .env file
    base_url = update_env_file()
    print(f"\n1. Updated .env with BASE_PUBLIC_URL={base_url}")
    
    # Create test driver
    print("\n2. Creating test driver...")
    
    import random
    random_num = random.randint(10000000, 99999999)
    data = {
        'name': f'Test Driver {random_num}',
        'phone': f'2547{random_num}',
        'email': f'driver{random_num}@gopay.com',
        'vehicle_type': 'boda',
        'vehicle_number': f'KAA{random_num}T'
    }
    
    response = requests.post('http://localhost:8000/api/register_driver', json=data)
    result = response.json()
    
    if 'driver_id' in result:
        driver_id = result['driver_id']
        print("\n[SUCCESS] Driver created!")
        print(f"\nDriver Details:")
        print(f"  Name: {data['name']}")
        print(f"  Phone: {data['phone']}")
        print(f"  Vehicle: {data['vehicle_type']} - {data['vehicle_number']}")
        
        print(f"\nDashboard URL (open on your computer):")
        print(f"  {base_url}/driver/{driver_id}/dashboard")
        
        print(f"\nPayment URLs (will work on your phone):")
        print(f"1. Basic URL:")
        print(f"   {base_url}/pay?driver_id={driver_id}")
        print(f"\n2. With phone pre-filled:")
        print(f"   {base_url}/pay?driver_id={driver_id}&phone={data['phone']}")
        
        print("\nInstructions:")
        print("1. Stop the current server (Ctrl+C)")
        print("2. Run this command:")
        print(f"   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        print("\n3. Open the Dashboard URL on your computer")
        print("4. Scan the QR code with your phone")
        print("5. The payment page should open on your phone!")
    else:
        print("\n[ERROR] Failed to create driver:")
        print(result)
    
    print("\n" + "=" * 70)

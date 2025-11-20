#!/usr/bin/env python3
"""Check environment variables for QR code generation"""

import os
import socket
from dotenv import load_dotenv
load_dotenv()

def get_local_ip():
    """Get the local IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

print("=" * 70)
print("ENVIRONMENT CHECK")
print("=" * 70)

# Check BASE_PUBLIC_URL
base_url = os.getenv('BASE_PUBLIC_URL')
print("\nBASE_PUBLIC_URL:")
print(f"  Current value: {base_url}")

# Get local IP
local_ip = get_local_ip()
expected_url = f"http://{local_ip}:8000"
print(f"  Expected value: {expected_url}")

if not base_url:
    print("\n[ERROR] BASE_PUBLIC_URL not set!")
    print("Add this line to your .env file:")
    print(f"BASE_PUBLIC_URL={expected_url}")
elif base_url != expected_url:
    print("\n[WARNING] BASE_PUBLIC_URL might be incorrect!")
    print(f"Current:  {base_url}")
    print(f"Expected: {expected_url}")
else:
    print("\n[OK] BASE_PUBLIC_URL is correctly set!")

print("\nTo fix:")
print("1. Stop the server (Ctrl+C)")
print("2. Add/update in .env file:")
print(f"   BASE_PUBLIC_URL={expected_url}")
print("3. Run server with:")
print(f"   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")

print("\n" + "=" * 70)

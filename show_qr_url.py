#!/usr/bin/env python3
"""Show what URL is in the QR code"""

# The QR code for the test driver contains this URL:
driver_id = "0d6a7a41-82b9-4654-ad24-2fd2c3fa8d11"

print("=" * 70)
print("QR CODE INFORMATION")
print("=" * 70)

print("\nCurrent QR Code URL (without BASE_PUBLIC_URL set):")
print(f"  None/pay?driver_id={driver_id}")
print("\n  [WARNING] This won't work! Needs BASE_PUBLIC_URL in .env")

print("\n" + "=" * 70)

print("\nWhat the QR Code SHOULD contain (for local testing):")
print(f"  http://localhost:8000/pay?driver_id={driver_id}")

print("\nWhat happens when scanned:")
print("  1. Phone camera opens browser")
print("  2. Loads payment page at the URL above")
print("  3. Shows driver info and payment form")
print("  4. Passenger enters amount and phone")
print("  5. M-Pesa STK push is sent")
print("  6. Payment completes")

print("\n" + "=" * 70)

print("\nTo test the payment page NOW (without QR code):")
print(f"  Open: http://localhost:8000/pay?driver_id={driver_id}")

print("\n" + "=" * 70)

print("\nTO FIX: Add this line to your .env file:")
print("  BASE_PUBLIC_URL=http://localhost:8000")

print("\nAfter adding, restart the server and register a new driver.")
print("The new driver's QR code will work correctly!")
print("=" * 70)


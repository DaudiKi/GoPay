# GoPay Dashboard Information Guide

## Overview
All dashboards are now live and accessible. Below is a detailed breakdown of what information is displayed on each dashboard.

---

## 1. Driver Dashboard
**URL:** `http://localhost:8000/driver/{driver_id}/dashboard`

### Information Displayed:

#### Header Section
- **Title:** "Driver Dashboard"
- **Welcome Message:** "Welcome back, {Driver Name}!"

#### Statistics Cards (3 Cards)
1. **Current Balance**
   - Shows: Driver's available balance in KES
   - Format: KES X,XXX.XX
   - Color: Blue

2. **Total Earnings**
   - Shows: Lifetime earnings for the driver
   - Format: KES X,XXX.XX
   - Color: Green

3. **Payment QR Code**
   - Shows: Scannable QR code for payments
   - Features:
     - QR code image (200x200px)
     - Download button for QR code
     - Links to payment page

#### Recent Transactions Table
Displays all driver transactions with the following columns:
- **Date:** Transaction date and time (YYYY-MM-DD HH:MM)
- **Passenger:** Passenger phone number
- **Amount:** Amount paid in KES
- **Status:** Transaction status (completed/pending/failed)
  - Green badge for completed
  - Yellow badge for pending
  - Red badge for failed
- **Receipt:** M-Pesa receipt number (if available)

---

## 2. Admin Dashboard
**URL:** `http://localhost:8000/admin/dashboard`

### Information Displayed:

#### Header Section
- **Title:** "Admin Dashboard"
- **Subtitle:** "System Overview and Statistics"

#### Statistics Cards (4 Cards)
1. **Total Revenue**
   - Shows: All-time platform revenue
   - Format: KES X,XXX.XX
   - Color: Green

2. **Platform Fees**
   - Shows: Total fees collected by platform
   - Format: KES X,XXX.XX
   - Color: Blue

3. **Total Transactions**
   - Shows: Number of all transactions
   - Format: Integer count
   - Color: Purple

4. **Active Drivers**
   - Shows: Number of registered drivers
   - Format: Integer count
   - Color: Orange

#### Search and Filter Tools
- **Search Bar:** Search transactions by any field
- **Status Filter:** Filter by transaction status
  - All Statuses
  - Completed
  - Pending
  - Failed

#### All Transactions Table
Displays all system transactions with columns:
- **Date:** Transaction date and time
- **Driver ID:** UUID of the driver
- **Passenger:** Passenger phone number
- **Amount:** Total amount paid
- **Platform Fee:** Fee charged by platform
- **Status:** Transaction status (with color badges)
- **Receipt:** M-Pesa receipt number

---

## 3. Payment Page (Customer-Facing)
**URL:** `http://localhost:8000/pay?driver_id={driver_id}`

### Information Displayed:

#### Header
- **Title:** "Pay for Your Ride"
- Blue header bar

#### Driver Information Section
- **Driver Name:** Full name of the driver
- **Vehicle Type:** Type of vehicle (boda/taxi/uber/bolt)
- **Vehicle Number:** Vehicle registration number

#### Payment Form
- **Amount Field**
  - Label: "Amount (KES)"
  - Input: Number field
  - Placeholder: "Enter amount"

- **Phone Number Field**
  - Label: "M-Pesa Phone Number"
  - Input: Tel field
  - Placeholder: "254XXXXXXXXX"
  - Format: Kenyan phone number

- **Pay Now Button**
  - Full-width blue button
  - Submits payment request

#### Payment Status Messages
- **Loading State:** Animated spinner with "Processing payment..."
- **Success Message:** Green alert - "Payment initiated! Please check your phone for the M-Pesa prompt."
- **Error Message:** Red alert with error details

---

## 4. API Documentation
**URL:** `http://localhost:8000/docs`

### Information Displayed:

Interactive Swagger UI with all API endpoints:

#### Driver Management
- `POST /api/register_driver` - Register new driver
- `GET /api/driver/{driver_id}` - Get driver details

#### Payment Operations
- `POST /api/pay` - Initiate M-Pesa payment
- `POST /api/mpesa/callback` - M-Pesa callback handler

#### Dashboard Endpoints
- `GET /driver/{driver_id}/dashboard` - Driver dashboard page
- `GET /admin/dashboard` - Admin dashboard page
- `GET /pay` - Payment page

#### Statistics
- `GET /api/admin/stats` - Get admin statistics

---

## Current System Status

### Database
- ✅ Supabase connected
- ✅ Tables created (drivers, transactions, admin_stats)
- ✅ RLS policies configured

### Storage
- ✅ QR codes bucket created
- ✅ Public access enabled
- ✅ Upload/download working

### Active Data
- **Drivers:** At least 1 test driver registered
- **QR Codes:** Generated and stored
- **Transactions:** Ready to accept payments

---

## Testing the System

### To Test Driver Registration:
1. Go to http://localhost:8000/docs
2. Try `POST /api/register_driver`
3. Submit driver details
4. Get driver_id and qr_code_url

### To Test Payment Flow:
1. Open payment page: http://localhost:8000/pay?driver_id={driver_id}
2. Enter amount and phone number
3. Click "Pay Now"
4. Check phone for M-Pesa prompt (if M-Pesa is configured)

### To View Statistics:
1. Driver view: http://localhost:8000/driver/{driver_id}/dashboard
2. Admin view: http://localhost:8000/admin/dashboard

---

## Color Scheme

### Status Indicators
- **Completed:** Green (#10B981)
- **Pending:** Yellow (#F59E0B)
- **Failed:** Red (#EF4444)

### Statistics Cards
- Balance/Fees: Blue (#2563EB)
- Revenue/Earnings: Green (#10B981)
- Transactions: Purple (#9333EA)
- Drivers: Orange (#F97316)

---

## Next Steps

1. **Configure M-Pesa:** Update `.env` with real M-Pesa credentials for live payments
2. **Create More Drivers:** Use API to register multiple drivers
3. **Test Transactions:** Make test payments through the payment page
4. **Monitor Dashboard:** Watch statistics update in real-time
5. **Production Deployment:** Deploy to cloud when ready

---

**All dashboards are fully functional and displaying complete information!** ✅


import os
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    Driver, Transaction, AdminStats, 
    DriverRegistration, PaymentRequest, MpesaCallback
)
from .supabase_util import SupabaseManager
from .mpesa import MpesaAPI
from .qr_utils import generate_payment_qr

# Initialize FastAPI app
app = FastAPI(title="GoPay Payment Aggregator")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Initialize M-Pesa API and Supabase
mpesa_api = MpesaAPI()
supabase_manager = SupabaseManager()

@app.post("/api/register_driver")
async def register_driver(driver_data: DriverRegistration) -> dict:
    """Register a new driver and generate their payment QR code."""
    try:
        # Create driver object
        driver = Driver(
            id="",  # Will be set by Supabase
            name=driver_data.name,
            phone=driver_data.phone,
            email=driver_data.email,
            vehicle_type=driver_data.vehicle_type,
            vehicle_number=driver_data.vehicle_number
        )
        
        # Save driver to Supabase
        driver_id = await supabase_manager.create_driver(driver)
        
        # Generate QR code
        qr_bytes = generate_payment_qr(driver_id)
        
        # Upload QR code to Supabase Storage
        qr_url = await supabase_manager.upload_qr_code(driver_id, qr_bytes)
        
        # Update driver with QR code URL
        await supabase_manager.update_driver(driver_id, {"qr_code_url": qr_url})
        
        return {
            "status": "success",
            "driver_id": driver_id,
            "qr_code_url": qr_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/driver/{driver_id}")
async def get_driver(driver_id: str) -> Driver:
    """Get driver details by ID."""
    driver = await supabase_manager.get_driver(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@app.get("/pay", response_class=HTMLResponse)
async def payment_page(request: Request, driver_id: str, phone: str = None):
    """Render payment page for a driver."""
    driver = await supabase_manager.get_driver(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    return templates.TemplateResponse(
        "pay.html",
        {
            "request": request, 
            "driver": driver,
            "passenger_phone": phone
        }
    )

@app.post("/api/pay")
async def initiate_payment(payment: PaymentRequest) -> dict:
    """Initiate M-Pesa STK push payment."""
    try:
        # Verify driver exists
        driver = await supabase_manager.get_driver(payment.driver_id)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
        
        # Calculate platform fee (0.5%)
        platform_fee = round(payment.amount * 0.005, 2)
        driver_amount = payment.amount - platform_fee
        
        # Create pending transaction
        transaction = Transaction(
            id="",  # Will be set by Supabase
            driver_id=payment.driver_id,
            passenger_phone=payment.passenger_phone,
            amount_paid=payment.amount,
            platform_fee=platform_fee,
            driver_amount=driver_amount,
            status="pending"
        )
        
        # Save transaction
        transaction_id = await supabase_manager.create_transaction(transaction)
        
        # Initiate STK Push
        stk_response = await mpesa_api.initiate_stk_push(
            phone_number=payment.passenger_phone,
            amount=payment.amount,
            reference_id=transaction_id
        )
        
        # Store checkout request ID for callback handling
        checkout_request_id = stk_response.get("CheckoutRequestID")
        if checkout_request_id:
            # Update transaction with checkout request ID
            await supabase_manager.update_transaction_checkout_id(transaction_id, checkout_request_id)
        
        return {
            "status": "success",
            "transaction_id": transaction_id,
            "checkout_request_id": checkout_request_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mpesa/callback")
async def mpesa_callback(callback_data: MpesaCallback) -> dict:
    """Handle M-Pesa payment callback."""
    try:
        # Update transaction status based on result code
        status = "completed" if callback_data.result_code == 0 else "failed"
        
        # Update transaction status and M-Pesa receipt in Supabase
        success = await supabase_manager.update_transaction_status(
            callback_data.checkout_request_id,
            status,
            callback_data.mpesa_receipt_number
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/driver/{driver_id}/dashboard", response_class=HTMLResponse)
async def driver_dashboard(request: Request, driver_id: str):
    """Render driver dashboard."""
    driver = await supabase_manager.get_driver(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    transactions = await supabase_manager.get_driver_transactions(driver_id)
    
    return templates.TemplateResponse(
        "driver_dashboard.html",
        {
            "request": request,
            "driver": driver,
            "transactions": transactions
        }
    )

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Render admin dashboard."""
    stats = await supabase_manager.get_admin_stats()
    transactions = await supabase_manager.get_all_transactions()
    
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {
            "request": request,
            "stats": stats,
            "transactions": transactions
        }
    )

@app.get("/api/admin/stats")
async def get_admin_stats() -> AdminStats:
    """Get admin statistics."""
    return await supabase_manager.get_admin_stats()

@app.get("/api/driver/{driver_id}/transactions")
async def get_driver_transactions(driver_id: str) -> List[Transaction]:
    """Get transactions for a specific driver."""
    return await supabase_manager.get_driver_transactions(driver_id)


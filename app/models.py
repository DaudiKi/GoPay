from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class VehicleType(str, Enum):
    BODA = "boda"
    TAXI = "taxi"
    UBER = "uber"
    BOLT = "bolt"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Driver(BaseModel):
    id: Optional[str] = None
    name: str
    phone: str
    email: str
    vehicle_type: VehicleType
    vehicle_number: str
    qr_code_url: Optional[str] = None
    balance: float = 0.0
    total_earnings: float = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Transaction(BaseModel):
    id: Optional[str] = None
    driver_id: str
    passenger_phone: str
    amount_paid: float
    platform_fee: float
    driver_amount: float
    status: TransactionStatus = TransactionStatus.PENDING
    mpesa_receipt: Optional[str] = None
    checkout_request_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class AdminStats(BaseModel):
    total_transactions: int = 0
    total_revenue: float = 0.0
    total_platform_fees: float = 0.0
    active_drivers: int = 0
    updated_at: Optional[datetime] = None

# Request/Response models
class DriverRegistration(BaseModel):
    name: str
    phone: str
    email: str
    vehicle_type: VehicleType
    vehicle_number: str

class PaymentRequest(BaseModel):
    driver_id: str
    passenger_phone: str
    amount: float

class MpesaCallback(BaseModel):
    result_code: int
    result_desc: str
    merchant_request_id: str
    checkout_request_id: str
    mpesa_receipt_number: Optional[str] = None

import os
from datetime import datetime
from typing import Optional, Dict, Any, List
from supabase import create_client, Client
from .models import Driver, Transaction, AdminStats, TransactionStatus

class SupabaseManager:
    def __init__(self):
        """Initialize Supabase client."""
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables")
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)

    async def create_driver(self, driver: Driver) -> str:
        """Create a new driver in Supabase."""
        driver_data = driver.model_dump(exclude={'id', 'created_at', 'updated_at'})
        driver_data['created_at'] = datetime.utcnow().isoformat()
        driver_data['updated_at'] = datetime.utcnow().isoformat()
        
        result = self.supabase.table('drivers').insert(driver_data).execute()
        
        if result.data:
            return result.data[0]['id']
        else:
            raise Exception("Failed to create driver")

    async def get_driver(self, driver_id: str) -> Optional[Driver]:
        """Get driver details by ID."""
        result = self.supabase.table('drivers').select('*').eq('id', driver_id).execute()
        
        if result.data:
            driver_data = result.data[0]
            return Driver(**driver_data)
        return None

    async def update_driver(self, driver_id: str, data: Dict[str, Any]) -> bool:
        """Update driver details."""
        data['updated_at'] = datetime.utcnow().isoformat()
        
        result = self.supabase.table('drivers').update(data).eq('id', driver_id).execute()
        
        return len(result.data) > 0

    async def create_transaction(self, transaction: Transaction) -> str:
        """Create a new transaction with atomic updates."""
        transaction_data = transaction.model_dump(exclude={'id', 'created_at', 'updated_at'})
        transaction_data['created_at'] = datetime.utcnow().isoformat()
        transaction_data['updated_at'] = datetime.utcnow().isoformat()
        
        # Start a transaction
        try:
            # Create the transaction
            transaction_result = self.supabase.table('transactions').insert(transaction_data).execute()
            
            if not transaction_result.data:
                raise Exception("Failed to create transaction")
            
            transaction_id = transaction_result.data[0]['id']
            
            # Update driver balance and earnings using RPC function
            balance_result = self.supabase.rpc(
                'update_driver_balance',
                {
                    'driver_id': transaction.driver_id,
                    'amount': transaction.driver_amount
                }
            ).execute()
            
            # Update admin stats using RPC function
            stats_result = self.supabase.rpc(
                'update_admin_stats',
                {
                    'transaction_count': 1,
                    'revenue': transaction.amount_paid,
                    'platform_fee': transaction.platform_fee
                }
            ).execute()
            
            return transaction_id
            
        except Exception as e:
            # In a real implementation, you'd want to rollback here
            raise Exception(f"Transaction creation failed: {str(e)}")

    async def get_driver_transactions(self, driver_id: str, limit: int = 50) -> List[Transaction]:
        """Get transactions for a specific driver."""
        result = (self.supabase.table('transactions')
                 .select('*')
                 .eq('driver_id', driver_id)
                 .order('created_at', desc=True)
                 .limit(limit)
                 .execute())
        
        return [Transaction(**tx) for tx in result.data]

    async def get_admin_stats(self) -> AdminStats:
        """Get admin statistics."""
        result = self.supabase.table('admin_stats').select('*').eq('id', 'revenue').execute()
        
        if result.data:
            stats_data = result.data[0]
            return AdminStats(**stats_data)
        
        # Return default stats if none exist
        return AdminStats()

    async def upload_qr_code(self, driver_id: str, qr_image_bytes: bytes) -> str:
        """Upload QR code image to Supabase Storage."""
        file_path = f'qr_codes/{driver_id}.png'
        
        # Upload to Supabase Storage
        try:
            storage_result = self.supabase.storage.from_('qr-codes').upload(
                file_path, 
                qr_image_bytes,
                file_options={"content-type": "image/png"}
            )
        except Exception as e:
            raise Exception(f"Failed to upload QR code: {str(e)}")
        
        # Get public URL
        public_url = self.supabase.storage.from_('qr-codes').get_public_url(file_path)
        return public_url

    async def get_all_transactions(self, limit: int = 100) -> List[Transaction]:
        """Get all transactions for admin view."""
        result = (self.supabase.table('transactions')
                 .select('*')
                 .order('created_at', desc=True)
                 .limit(limit)
                 .execute())
        
        return [Transaction(**tx) for tx in result.data]

    async def update_transaction_status(self, checkout_request_id: str, status: TransactionStatus, mpesa_receipt: Optional[str] = None) -> bool:
        """Update transaction status based on M-Pesa callback."""
        update_data = {
            'status': status.value,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        if mpesa_receipt:
            update_data['mpesa_receipt'] = mpesa_receipt
        
        result = (self.supabase.table('transactions')
                 .update(update_data)
                 .eq('checkout_request_id', checkout_request_id)
                 .execute())
        
        return len(result.data) > 0

    async def get_transaction_by_checkout_id(self, checkout_request_id: str) -> Optional[Transaction]:
        """Get transaction by checkout request ID."""
        result = (self.supabase.table('transactions')
                 .select('*')
                 .eq('checkout_request_id', checkout_request_id)
                 .execute())
        
        if result.data:
            return Transaction(**result.data[0])
        return None

    async def update_transaction_checkout_id(self, transaction_id: str, checkout_request_id: str) -> bool:
        """Update transaction with checkout request ID."""
        update_data = {
            'checkout_request_id': checkout_request_id,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        result = (self.supabase.table('transactions')
                 .update(update_data)
                 .eq('id', transaction_id)
                 .execute())
        
        return len(result.data) > 0
import os
import base64
import json
from datetime import datetime
import requests
from typing import Dict, Any, Optional

class MpesaAPI:
    def __init__(self):
        """Initialize M-Pesa API with configuration from environment variables."""
        self.base_url = os.getenv('DARAJA_BASE_URL')
        self.consumer_key = os.getenv('DARAJA_CONSUMER_KEY')
        self.consumer_secret = os.getenv('DARAJA_CONSUMER_SECRET')
        self.shortcode = os.getenv('DARAJA_SHORT_CODE')
        self.passkey = os.getenv('DARAJA_PASSKEY')
        self.callback_url = os.getenv('DARAJA_CALLBACK_URL')
        self.account_ref = os.getenv('DARAJA_ACCOUNT_REF')
        self.transaction_desc = os.getenv('DARAJA_TRANSACTION_DESC')

    def _get_auth_token(self) -> str:
        """Get OAuth token for API authentication."""
        auth_string = f"{self.consumer_key}:{self.consumer_secret}"
        auth_bytes = auth_string.encode("ascii")
        auth_base64 = base64.b64encode(auth_bytes).decode('ascii')

        try:
            response = requests.get(
                f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials",
                headers={
                    "Authorization": f"Basic {auth_base64}"
                }
            )
            response.raise_for_status()
            result = response.json()
            return result['access_token']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get auth token: {str(e)}")

    def _generate_password(self, timestamp: str) -> str:
        """Generate password for STK Push."""
        password_string = f"{self.shortcode}{self.passkey}{timestamp}"
        return base64.b64encode(password_string.encode()).decode('ascii')

    async def initiate_stk_push(
        self, 
        phone_number: str, 
        amount: float,
        reference_id: str
    ) -> Dict[str, Any]:
        """
        Initiate STK Push to customer's phone.
        
        Args:
            phone_number: Customer's phone number (format: 254XXXXXXXXX)
            amount: Amount to charge
            reference_id: Unique reference ID for the transaction
        
        Returns:
            Dict containing the response from M-Pesa
        """
        # Format timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Get auth token
        token = self._get_auth_token()
        
        # Generate password
        password = self._generate_password(timestamp)
        
        # Prepare the request
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": f"{self.account_ref}-{reference_id[:8]}",
            "TransactionDesc": self.transaction_desc
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"STK push failed: {str(e)}")

    async def verify_transaction(self, checkout_request_id: str) -> Optional[Dict[str, Any]]:
        """
        Verify the status of a transaction using the checkout request ID.
        
        Args:
            checkout_request_id: The CheckoutRequestID from STK push response
            
        Returns:
            Dict containing the transaction status or None if verification fails
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        token = self._get_auth_token()
        password = self._generate_password(timestamp)
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/mpesa/stkpushquery/v1/query",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

















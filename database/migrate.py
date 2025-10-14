#!/usr/bin/env python3
"""
Database migration script for GoPay Supabase setup.
This script helps migrate data from Firebase to Supabase.
"""

import os
import asyncio
from datetime import datetime
from typing import List, Dict, Any
from supabase import create_client, Client
import json

# You'll need to install firebase-admin for this migration
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("Firebase admin not available. Install with: pip install firebase-admin")

class DatabaseMigrator:
    def __init__(self, supabase_url: str, supabase_key: str, firebase_credentials_path: str = None):
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.firebase_db = None
        
        if FIREBASE_AVAILABLE and firebase_credentials_path:
            # Initialize Firebase
            cred = credentials.Certificate(firebase_credentials_path)
            firebase_admin.initialize_app(cred)
            self.firebase_db = firestore.client()

    async def migrate_drivers(self) -> int:
        """Migrate drivers from Firebase to Supabase."""
        if not self.firebase_db:
            print("Firebase not available. Skipping driver migration.")
            return 0
        
        print("Migrating drivers...")
        drivers_ref = self.firebase_db.collection('drivers')
        docs = drivers_ref.stream()
        
        migrated_count = 0
        for doc in docs:
            driver_data = doc.to_dict()
            
            # Convert Firebase data to Supabase format
            supabase_driver = {
                'id': doc.id,
                'name': driver_data.get('name', ''),
                'phone': driver_data.get('phone', ''),
                'email': driver_data.get('email', ''),
                'vehicle_type': driver_data.get('vehicle_type', 'boda'),
                'vehicle_number': driver_data.get('vehicle_number', ''),
                'qr_code_url': driver_data.get('qr_code_url'),
                'balance': float(driver_data.get('balance', 0)),
                'total_earnings': float(driver_data.get('total_earnings', 0)),
                'created_at': driver_data.get('created_at').isoformat() if driver_data.get('created_at') else datetime.utcnow().isoformat(),
                'updated_at': driver_data.get('updated_at').isoformat() if driver_data.get('updated_at') else datetime.utcnow().isoformat()
            }
            
            try:
                # Insert into Supabase
                result = self.supabase.table('drivers').insert(supabase_driver).execute()
                if result.data:
                    migrated_count += 1
                    print(f"Migrated driver: {driver_data.get('name', 'Unknown')}")
            except Exception as e:
                print(f"Error migrating driver {doc.id}: {str(e)}")
        
        print(f"Migrated {migrated_count} drivers")
        return migrated_count

    async def migrate_transactions(self) -> int:
        """Migrate transactions from Firebase to Supabase."""
        if not self.firebase_db:
            print("Firebase not available. Skipping transaction migration.")
            return 0
        
        print("Migrating transactions...")
        transactions_ref = self.firebase_db.collection('transactions')
        docs = transactions_ref.stream()
        
        migrated_count = 0
        for doc in docs:
            transaction_data = doc.to_dict()
            
            # Convert Firebase data to Supabase format
            supabase_transaction = {
                'id': doc.id,
                'driver_id': transaction_data.get('driver_id', ''),
                'passenger_phone': transaction_data.get('passenger_phone', ''),
                'amount_paid': float(transaction_data.get('amount_paid', 0)),
                'platform_fee': float(transaction_data.get('platform_fee', 0)),
                'driver_amount': float(transaction_data.get('driver_amount', 0)),
                'status': transaction_data.get('status', 'pending'),
                'mpesa_receipt': transaction_data.get('mpesa_receipt'),
                'checkout_request_id': transaction_data.get('checkout_request_id'),
                'created_at': transaction_data.get('created_at').isoformat() if transaction_data.get('created_at') else datetime.utcnow().isoformat(),
                'updated_at': transaction_data.get('updated_at').isoformat() if transaction_data.get('updated_at') else datetime.utcnow().isoformat()
            }
            
            try:
                # Insert into Supabase
                result = self.supabase.table('transactions').insert(supabase_transaction).execute()
                if result.data:
                    migrated_count += 1
                    print(f"Migrated transaction: {doc.id}")
            except Exception as e:
                print(f"Error migrating transaction {doc.id}: {str(e)}")
        
        print(f"Migrated {migrated_count} transactions")
        return migrated_count

    async def migrate_admin_stats(self) -> int:
        """Migrate admin stats from Firebase to Supabase."""
        if not self.firebase_db:
            print("Firebase not available. Skipping admin stats migration.")
            return 0
        
        print("Migrating admin stats...")
        stats_ref = self.firebase_db.collection('adminStats').document('revenue')
        doc = stats_ref.get()
        
        if doc.exists:
            stats_data = doc.to_dict()
            
            supabase_stats = {
                'id': 'revenue',
                'total_transactions': stats_data.get('total_transactions', 0),
                'total_revenue': float(stats_data.get('total_revenue', 0)),
                'total_platform_fees': float(stats_data.get('total_platform_fees', 0)),
                'active_drivers': stats_data.get('active_drivers', 0),
                'updated_at': stats_data.get('updated_at').isoformat() if stats_data.get('updated_at') else datetime.utcnow().isoformat()
            }
            
            try:
                # Insert into Supabase
                result = self.supabase.table('admin_stats').upsert(supabase_stats).execute()
                if result.data:
                    print("Migrated admin stats")
                    return 1
            except Exception as e:
                print(f"Error migrating admin stats: {str(e)}")
        
        return 0

    async def run_migration(self):
        """Run the complete migration process."""
        print("Starting database migration from Firebase to Supabase...")
        
        # Run migrations
        drivers_count = await self.migrate_drivers()
        transactions_count = await self.migrate_transactions()
        stats_count = await self.migrate_admin_stats()
        
        print(f"\nMigration completed!")
        print(f"- Drivers migrated: {drivers_count}")
        print(f"- Transactions migrated: {transactions_count}")
        print(f"- Admin stats migrated: {stats_count}")

async def main():
    """Main migration function."""
    # Get environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    firebase_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        return
    
    if not firebase_credentials:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS not set. Firebase migration will be skipped.")
    
    # Create migrator
    migrator = DatabaseMigrator(supabase_url, supabase_key, firebase_credentials)
    
    # Run migration
    await migrator.run_migration()

if __name__ == "__main__":
    asyncio.run(main())

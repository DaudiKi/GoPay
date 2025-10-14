-- GoPay Supabase Database Schema
-- This file contains the SQL schema for the GoPay payment aggregator

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
CREATE TYPE vehicle_type AS ENUM ('boda', 'taxi', 'uber', 'bolt');
CREATE TYPE transaction_status AS ENUM ('pending', 'completed', 'failed', 'cancelled');

-- Drivers table
CREATE TABLE drivers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    vehicle_type vehicle_type NOT NULL,
    vehicle_number VARCHAR(50) NOT NULL,
    qr_code_url TEXT,
    balance DECIMAL(10,2) DEFAULT 0.00,
    total_earnings DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transactions table
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    driver_id UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    passenger_phone VARCHAR(20) NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL,
    platform_fee DECIMAL(10,2) NOT NULL,
    driver_amount DECIMAL(10,2) NOT NULL,
    status transaction_status DEFAULT 'pending',
    mpesa_receipt VARCHAR(100),
    checkout_request_id VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Admin stats table
CREATE TABLE admin_stats (
    id VARCHAR(50) PRIMARY KEY DEFAULT 'revenue',
    total_transactions INTEGER DEFAULT 0,
    total_revenue DECIMAL(15,2) DEFAULT 0.00,
    total_platform_fees DECIMAL(15,2) DEFAULT 0.00,
    active_drivers INTEGER DEFAULT 0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_drivers_phone ON drivers(phone);
CREATE INDEX idx_drivers_email ON drivers(email);
CREATE INDEX idx_transactions_driver_id ON transactions(driver_id);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);
CREATE INDEX idx_transactions_checkout_request_id ON transactions(checkout_request_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_drivers_updated_at BEFORE UPDATE ON drivers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_transactions_updated_at BEFORE UPDATE ON transactions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_admin_stats_updated_at BEFORE UPDATE ON admin_stats
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create RPC functions for atomic operations
CREATE OR REPLACE FUNCTION update_driver_balance(driver_id UUID, amount DECIMAL)
RETURNS VOID AS $$
BEGIN
    UPDATE drivers 
    SET 
        balance = balance + amount,
        total_earnings = total_earnings + amount,
        updated_at = NOW()
    WHERE id = driver_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_admin_stats(
    transaction_count INTEGER,
    revenue DECIMAL,
    platform_fee DECIMAL
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO admin_stats (id, total_transactions, total_revenue, total_platform_fees, updated_at)
    VALUES ('revenue', transaction_count, revenue, platform_fee, NOW())
    ON CONFLICT (id) DO UPDATE SET
        total_transactions = admin_stats.total_transactions + transaction_count,
        total_revenue = admin_stats.total_revenue + revenue,
        total_platform_fees = admin_stats.total_platform_fees + platform_fee,
        updated_at = NOW();
END;
$$ LANGUAGE plpgsql;

-- Create function to get active drivers count
CREATE OR REPLACE FUNCTION get_active_drivers_count()
RETURNS INTEGER AS $$
BEGIN
    RETURN (SELECT COUNT(*) FROM drivers WHERE created_at > NOW() - INTERVAL '30 days');
END;
$$ LANGUAGE plpgsql;

-- Create function to update active drivers count
CREATE OR REPLACE FUNCTION update_active_drivers_count()
RETURNS VOID AS $$
BEGIN
    UPDATE admin_stats 
    SET 
        active_drivers = get_active_drivers_count(),
        updated_at = NOW()
    WHERE id = 'revenue';
END;
$$ LANGUAGE plpgsql;

-- Insert initial admin stats record
INSERT INTO admin_stats (id, total_transactions, total_revenue, total_platform_fees, active_drivers)
VALUES ('revenue', 0, 0.00, 0.00, 0)
ON CONFLICT (id) DO NOTHING;

-- Create storage bucket for QR codes
INSERT INTO storage.buckets (id, name, public)
VALUES ('qr-codes', 'qr-codes', true)
ON CONFLICT (id) DO NOTHING;

-- Set up Row Level Security (RLS) policies
ALTER TABLE drivers ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_stats ENABLE ROW LEVEL SECURITY;

-- Allow all operations for now (you can restrict this later based on your auth requirements)
CREATE POLICY "Allow all operations on drivers" ON drivers FOR ALL USING (true);
CREATE POLICY "Allow all operations on transactions" ON transactions FOR ALL USING (true);
CREATE POLICY "Allow all operations on admin_stats" ON admin_stats FOR ALL USING (true);

-- Grant necessary permissions
GRANT ALL ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO postgres;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO postgres;

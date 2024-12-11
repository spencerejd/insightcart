-- Change from private to public schema
CREATE SCHEMA IF NOT EXISTS public;
CREATE SCHEMA IF NOT EXISTS demo;

-- Base tables in public schema (changed from private)
CREATE TABLE transactions (
    id VARCHAR PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(50) NOT NULL,
    payment_type VARCHAR(50) NOT NULL,
    card_type VARCHAR(50),
    entry_mode VARCHAR(50),
    merchant_code VARCHAR(50) NOT NULL,
    username VARCHAR(255) NOT NULL,
    auth_code VARCHAR(50),
    installments_count INTEGER DEFAULT 1,
    tip_amount DECIMAL(10,2) DEFAULT 0,
    vat_amount DECIMAL(10,2) DEFAULT 0,
    tax_enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE locations (
    transaction_id VARCHAR PRIMARY KEY REFERENCES transactions(id),
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    horizontal_accuracy DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    standard_price DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name)
);

CREATE TABLE transaction_products (
    transaction_id VARCHAR REFERENCES transactions(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    vat_amount DECIMAL(10,2) DEFAULT 0,
    vat_rate DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (transaction_id, product_id)
);

CREATE TABLE payouts (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR REFERENCES transactions(id),
    amount DECIMAL(10,2) NOT NULL,
    fee_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    payout_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


-- Create equivalent tables in demo schema
CREATE TABLE demo.transactions (
    LIKE transactions INCLUDING ALL
);

CREATE TABLE demo.locations (
    LIKE locations INCLUDING ALL
);

CREATE TABLE demo.products (
    LIKE products INCLUDING ALL
);

CREATE TABLE demo.transaction_products (
    LIKE transaction_products INCLUDING ALL
);

CREATE TABLE demo.payouts (
    LIKE payouts INCLUDING ALL
);

-- Row Level Security Policies
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE locations ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE transaction_products ENABLE ROW LEVEL SECURITY;
ALTER TABLE payouts ENABLE ROW LEVEL SECURITY;

ALTER TABLE demo.transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE demo.locations ENABLE ROW LEVEL SECURITY;
ALTER TABLE demo.products ENABLE ROW LEVEL SECURITY;
ALTER TABLE demo.transaction_products ENABLE ROW LEVEL SECURITY;
ALTER TABLE demo.payouts ENABLE ROW LEVEL SECURITY;

-- Only authenticated business owner can access public schema (changed from private)
CREATE POLICY "Full access for business owner" ON transactions
    FOR ALL
    TO authenticated
    USING (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'))
    WITH CHECK (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'));

CREATE POLICY "Full access for business owner" ON locations
    FOR ALL
    TO authenticated
    USING (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'))
    WITH CHECK (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'));

CREATE POLICY "Full access for business owner" ON products
    FOR ALL
    TO authenticated
    USING (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'))
    WITH CHECK (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'));

CREATE POLICY "Full access for business owner" ON transaction_products
    FOR ALL
    TO authenticated
    USING (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'))
    WITH CHECK (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'));

CREATE POLICY "Full access for business owner" ON payouts
    FOR ALL
    TO authenticated
    USING (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'))
    WITH CHECK (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'));

-- Only authenticated business owner can access demo schema
CREATE POLICY "Full access for business owner" ON demo.transactions
    FOR ALL
    TO authenticated
    USING (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'))
    WITH CHECK (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'));

CREATE POLICY "Full access for business owner" ON demo.locations
    FOR ALL
    TO authenticated
    USING (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'))
    WITH CHECK (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'));

CREATE POLICY "Full access for business owner" ON demo.products
    FOR ALL
    TO authenticated
    USING (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'))
    WITH CHECK (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'));

CREATE POLICY "Full access for business owner" ON demo.transaction_products
    FOR ALL
    TO authenticated
    USING (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'))
    WITH CHECK (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'));

CREATE POLICY "Full access for business owner" ON demo.payouts
    FOR ALL
    TO authenticated
    USING (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'))
    WITH CHECK (auth.uid() IN (SELECT id FROM auth.users WHERE email = 'business_owner@example.com'));


-- Create indexes for frequently accessed columns in schema

-- Transaction-related indexes
CREATE INDEX idx_transactions_timestamp_amount ON transactions(timestamp, amount);
CREATE INDEX idx_transactions_status ON transactions(status);

-- Location index for geographical analysis
CREATE INDEX idx_locations_coords ON locations(latitude, longitude);

-- Product sales analysis index
-- Enables better handling of queries that might be affected by change in prices
CREATE INDEX idx_transaction_products_composite ON transaction_products(product_id, unit_price, total_price);


-- Create indexes for demo schema

-- Transaction-related indexes
CREATE INDEX idx_demo_transactions_timestamp_amount ON demo.transactions(timestamp, amount);
CREATE INDEX idx_demo_transactions_status ON demo.transactions(status);

-- Location index for geographical analysis
CREATE INDEX idx_demo_locations_coords ON demo.locations(latitude, longitude);

-- Product sales analysis index
-- Enables better handling of queries that might be affected by change in prices
CREATE INDEX idx_demo_transaction_products_composite ON demo.transaction_products(product_id, unit_price, total_price);
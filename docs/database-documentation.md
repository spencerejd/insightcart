# InsightCart Database Schema Documentation

**Last Updated:** 9 December 2024  
**Project:** InsightCart MVP  
**Database:** Supabase PostgreSQL  
**Schema Version:** 1.0

## Overview
This document outlines the database schema for the InsightCart MVP, designed to store and manage transaction data from SumUp POS systems. The schema is implemented in Supabase and includes security measures for data protection.

## Schema Structure
All tables are housed in the `private` schema to ensure data security.

### Tables

#### transactions
Primary table for storing transaction records from SumUp.

| Column Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | VARCHAR | Unique transaction identifier | PRIMARY KEY |
| timestamp | TIMESTAMP WITH TIME ZONE | Transaction date and time | NOT NULL |
| amount | DECIMAL(10,2) | Transaction amount | NOT NULL |
| currency | VARCHAR(3) | Currency code | NOT NULL |
| status | VARCHAR(50) | Transaction status | NOT NULL |
| payment_type | VARCHAR(50) | Method of payment | NOT NULL |
| card_type | VARCHAR(50) | Type of card used | NULLABLE |
| entry_mode | VARCHAR(50) | Payment entry method | NULLABLE |
| merchant_code | VARCHAR(50) | SumUp merchant identifier | NOT NULL |
| username | VARCHAR(255) | Merchant username | NOT NULL |
| auth_code | VARCHAR(50) | Authorization code | NULLABLE |
| installments_count | INTEGER | Number of installments | DEFAULT 1 |
| tip_amount | DECIMAL(10,2) | Tip amount | DEFAULT 0 |
| vat_amount | DECIMAL(10,2) | VAT amount | DEFAULT 0 |
| tax_enabled | BOOLEAN | Tax calculation flag | DEFAULT true |
| created_at | TIMESTAMP WITH TIME ZONE | Record creation timestamp | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP WITH TIME ZONE | Record update timestamp | DEFAULT CURRENT_TIMESTAMP |

#### locations
Stores geographical data for transactions.

| Column Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| transaction_id | VARCHAR | Reference to transaction | PRIMARY KEY, FOREIGN KEY |
| latitude | DECIMAL(10,8) | Location latitude | NOT NULL |
| longitude | DECIMAL(11,8) | Location longitude | NOT NULL |
| horizontal_accuracy | DECIMAL(10,2) | Location accuracy | NULLABLE |
| created_at | TIMESTAMP WITH TIME ZONE | Record creation timestamp | DEFAULT CURRENT_TIMESTAMP |

#### products
Catalogue of available products.

| Column Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | SERIAL | Product identifier | PRIMARY KEY |
| name | VARCHAR(255) | Product name | NOT NULL, UNIQUE |
| description | TEXT | Product description | NULLABLE |
| standard_price | DECIMAL(10,2) | Standard price | NULLABLE |
| created_at | TIMESTAMP WITH TIME ZONE | Record creation timestamp | DEFAULT CURRENT_TIMESTAMP |

#### transaction_products
Junction table linking transactions to products.

| Column Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| transaction_id | VARCHAR | Reference to transaction | FOREIGN KEY |
| product_id | INTEGER | Reference to product | FOREIGN KEY |
| quantity | INTEGER | Quantity purchased | NOT NULL |
| unit_price | DECIMAL(10,2) | Price per unit | NOT NULL |
| total_price | DECIMAL(10,2) | Total line item price | NOT NULL |
| vat_amount | DECIMAL(10,2) | VAT amount | DEFAULT 0 |
| vat_rate | DECIMAL(5,2) | VAT rate applied | DEFAULT 0 |
| created_at | TIMESTAMP WITH TIME ZONE | Record creation timestamp | DEFAULT CURRENT_TIMESTAMP |

#### payouts
Records of merchant payouts.

| Column Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | SERIAL | Payout identifier | PRIMARY KEY |
| transaction_id | VARCHAR | Reference to transaction | FOREIGN KEY |
| amount | DECIMAL(10,2) | Payout amount | NOT NULL |
| fee_amount | DECIMAL(10,2) | Processing fee | NOT NULL |
| status | VARCHAR(50) | Payout status | NOT NULL |
| payout_date | DATE | Date of payout | NULLABLE |
| created_at | TIMESTAMP WITH TIME ZONE | Record creation timestamp | DEFAULT CURRENT_TIMESTAMP |

## Security Implementation

### Row Level Security (RLS)
- RLS is enabled on all tables in the private schema
- Access is restricted to authenticated business owner
- Authentication is managed through Supabase auth system

### Access Policies
- Full access (SELECT, INSERT, UPDATE, DELETE) granted only to authenticated business owner
- No public access to any tables
- Data anonymisation will be handled at the application level

## Data Flow
1. Raw transaction data from SumUp API
2. Stored in private schema tables
3. Anonymisation performed in application layer
4. Visualisations created from anonymised data

## Maintenance Notes
- Regular backups managed by Supabase
- Schema updates should be documented with version control
- New columns should maintain backwards compatibility

## Future Considerations
1. Add indices for frequently queried columns
2. Implement table partitioning if data volume grows
3. Add audit logging for sensitive operations
4. Consider archival strategy for historical data

## Change Log
- 2024-12-09: Initial schema creation and documentation

# SumUp API Fields Documentation

**Last Updated:** 9 December 2024  
**API Version:** v0.1 (based on endpoint paths used)  
**Documentation Status:** Active  
**Tested With:** SumUp REST API (accessing via `api.sumup.com/v0.1/`)

> **Note:** This documentation reflects the SumUp API as tested on the above date. Please verify endpoint behaviour and available fields if accessing this document after this date.

## Overview
The SumUp API provides two main endpoints for accessing transaction data, each offering different levels of detail:
1. Transaction History Endpoint (`/v0.1/me/transactions/history`)
2. Single Transaction Endpoint (`/v0.1/me/transactions`)

## Transaction History Endpoint Fields
Basic transaction information available when querying multiple transactions:

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| amount | float | Transaction amount |
| card_type | string | Type of card used (e.g., VISA, MASTERCARD, AMEX) |
| client_transaction_id | string | Client-specific transaction identifier |
| currency | string | Transaction currency code |
| entry_mode | string | Method of payment entry |
| id | string | Unique transaction identifier |
| installments_count | integer | Number of installments (if applicable) |
| payment_type | string | Type of payment |
| payout_date | string | Date when payout was processed |
| payout_plan | string | Plan for merchant payout |
| payout_type | string | Type of payout |
| payouts_received | integer | Number of payouts received |
| payouts_total | integer | Total number of payouts |
| refunded_amount | integer | Amount refunded (if applicable) |
| status | string | Transaction status |
| timestamp | string | Transaction timestamp |
| transaction_code | string | SumUp transaction code |
| transaction_id | string | Alternative transaction identifier |
| type | string | Transaction type |
| user | string | User associated with transaction |

## Single Transaction Endpoint Additional Fields
Additional detailed information available when querying individual transactions:

### Core Fields
| Field Name | Data Type | Description |
|------------|-----------|-------------|
| auth_code | string | Authorization code |
| internal_id | integer | Internal SumUp identifier |
| local_time | string | Transaction time in local timezone |
| merchant_code | string | Merchant identifier |
| simple_payment_type | string | Simplified payment type classification |
| simple_status | string | Simplified transaction status |
| tax_enabled | boolean | Whether tax calculation is enabled |
| username | string | Username of merchant |
| verification_method | string | Method used to verify payment |

### Location Data
| Field Name | Data Type | Description |
|------------|-----------|-------------|
| horizontal_accuracy | float | Location accuracy measurement |
| lat | float | Latitude coordinate |
| lon | float | Longitude coordinate |
| location | object | Composite location object |

### Financial Details
| Field Name | Data Type | Description |
|------------|-----------|-------------|
| tip_amount | float | Amount of tip included |
| vat_amount | float | VAT amount |
| vat_rates | array | Applied VAT rates |

### Related Objects
| Field Name | Data Type | Description |
|------------|-----------|-------------|
| card | object | Detailed card information (includes last_4_digits and type) |
| events | array | List of transaction events |
| links | array | Related resource links |
| products | array | List of products in transaction |
| transaction_events | array | Detailed transaction event history |

## Product Information Structure
When available, product information includes:
- price (float)
- quantity (integer)
- total_price (float)

## Notes
1. All monetary values are provided as floats in the transaction currency
2. Timestamps follow ISO8601 format
3. Location data appears to have standard precision (32.0 horizontal accuracy)
4. Card information is partially masked for security (only last 4 digits available)

## Change Log
- 2024-12-09: Initial documentation created based on API investigation
  - Documented fields from transaction history endpoint
  - Documented additional fields from single transaction endpoint
  - Added examples of data types and field structures
  - Verified location data availability and precision

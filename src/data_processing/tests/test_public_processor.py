"""
Unit tests for the DataProcessor class in the src.data_processing.public_processor module.
"""

from datetime import datetime, timezone
import pytest
from src.data_processing.public_processor import DataProcessor


class TestDataProcessor:
    """Unit tests for the DataProcessor class."""

    @pytest.fixture
    def mock_transaction_data(self):
        """Generate mock transaction data for testing"""
        return [
            {
                "id": "mock-transaction-001",
                "timestamp": "2024-01-15T14:30:00Z",
                "amount": 25.50,
                "currency": "GBP",
                "status": "SUCCESSFUL",
                "payment_type": "CARD",
                "card_type": "VISA",
                "lat": 51.5074,
                "lon": -0.1278,
                "merchant_code": "MOCK001",
                "entry_mode": "contactless",
                "username": "mock.merchant@example.com",
                "products": [
                    {"name": "Sample Product A", "price": 15.50, "quantity": 1},
                    {"name": "Sample Product B", "price": 10.00, "quantity": 1},
                ],
            }
        ]

    def test_standardise_timestamp(self):
        """Test the standardisation of timestamps."""
        processor = DataProcessor()

        # Test with string timestamp
        test_timestamp = "2024-01-15T14:30:00Z"
        result = processor.standardise_timestamp(test_timestamp)
        assert isinstance(result, datetime)
        assert result.tzinfo == timezone.utc

        # Test with datetime object
        test_datetime = datetime.now()
        result = processor.standardise_timestamp(test_datetime)
        assert isinstance(result, datetime)
        assert result.tzinfo == timezone.utc

        # Test invalid format
        with pytest.raises(ValueError):
            processor.standardise_timestamp("invalid-date")

    def test_extract_time_features(self, mock_transaction_data):
        """Test the extraction of time features from a standardized timestamp."""
        processor = DataProcessor()

        # Test with mock transaction
        timestamp = processor.standardise_timestamp(
            mock_transaction_data[0]["timestamp"]
        )
        features = processor.extract_time_features(timestamp)

        # Our mock date is 2024-01-15 14:30:00 (Monday)
        assert features["hour"] == 14
        assert features["day_of_week"] == 0  # Monday
        assert features["day_of_month"] == 15
        assert features["month"] == 1
        assert features["quarter"] == 1
        assert features["year"] == 2024
        assert features["is_weekend"] is False
        assert features["is_business_hours"] is True

    def test_validate_coordinates(self):
        """Test the validation of geographical coordinates."""
        processor = DataProcessor()

        # Test valid coordinates (London)
        assert processor.validate_coordinates(51.5074, -0.1278) is True

        # Test boundary cases
        assert processor.validate_coordinates(90, 180) is True
        assert processor.validate_coordinates(-90, -180) is True

        # Test invalid coordinates
        assert processor.validate_coordinates(91, 0) is False
        assert processor.validate_coordinates(0, 181) is False
        assert processor.validate_coordinates("invalid", 0) is False
        assert processor.validate_coordinates(None, None) is False

    def test_validate_currency_amount(self):
        """Test the validation of currency amounts."""
        processor = DataProcessor()

        # Test valid amounts
        assert processor.validate_currency_amount(25.50) == 25.50
        assert processor.validate_currency_amount("25.50") == 25.50
        assert processor.validate_currency_amount("1,234.56") == 1234.56
        assert processor.validate_currency_amount(0) == 0.00

        # Test rounding
        assert processor.validate_currency_amount(10.999) == 11.00
        assert processor.validate_currency_amount(10.001) == 10.00

        # Test invalid amounts
        assert processor.validate_currency_amount("invalid") is None
        assert processor.validate_currency_amount(None) is None
        assert processor.validate_currency_amount("") is None

    def test_validate_required_fields(self):
        """Test the validation of required fields in transaction data."""
        processor = DataProcessor()

        # Test with complete data
        complete_data = {
            "id": "123",
            "timestamp": "2024-01-01",
            "amount": 10.00,
            "status": "SUCCESSFUL",
        }
        required_fields = ["id", "timestamp", "amount", "status"]
        assert (
            processor.validate_required_fields(complete_data, required_fields) is True
        )

        # Test with missing field
        incomplete_data = {"id": "123", "timestamp": "2024-01-01"}
        assert (
            processor.validate_required_fields(incomplete_data, required_fields)
            is False
        )

        # Test with null value
        null_data = {
            "id": "123",
            "timestamp": None,
            "amount": 10.00,
            "status": "SUCCESSFUL",
        }
        assert processor.validate_required_fields(null_data, required_fields) is False

    def test_standardise_payment_type(self):
        """Test the standardisation of payment types."""
        processor = DataProcessor()

        # Test standard payment types
        assert processor.standardise_payment_type("CASH") == "CASH"
        assert processor.standardise_payment_type("POS") == "CARD"
        assert processor.standardise_payment_type("CONTACTLESS") == "CARD"

        # Test variations
        assert processor.standardise_payment_type("cash payment") == "CASH"
        assert processor.standardise_payment_type("CARD_PAYMENT") == "CARD"
        assert processor.standardise_payment_type("  CASH  ") == "CASH"

        # Test fallback
        assert processor.standardise_payment_type("UNKNOWN") == "OTHER"
        assert processor.standardise_payment_type("") == "OTHER"

    def test_calculate_derived_amounts(self):
        """Test the calculation of derived amounts including gross, net, VAT, and fees."""
        processor = DataProcessor()

        # Test without VAT or fees
        result = processor.calculate_derived_amounts(100.00)
        assert result["gross_amount"] == 100.00
        assert result["net_amount"] == 100.00
        assert result["vat_amount"] == 0.00

        # Test with VAT only (20%)
        result = processor.calculate_derived_amounts(120.00, vat_rate=0.20)
        assert result["gross_amount"] == 120.00
        assert result["vat_amount"] == pytest.approx(20.00, rel=1e-2)
        assert result["net_amount"] == pytest.approx(100.00, rel=1e-2)

        # Test with VAT and fees
        result = processor.calculate_derived_amounts(
            120.00, vat_rate=0.20, fee_rate=0.015
        )
        assert result["gross_amount"] == 120.00
        assert result["vat_amount"] == pytest.approx(20.00, rel=1e-2)
        assert result["net_amount"] == pytest.approx(100.00, rel=1e-2)
        assert result["fee_amount"] == pytest.approx(1.50, rel=1e-2)
        assert result["settlement_amount"] == pytest.approx(98.50, rel=1e-2)


if __name__ == "__main__":
    pytest.main([__file__])

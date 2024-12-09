"""
Module for public data processing, including functions for cleaning, validation, and feature extraction.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, Union
import pandas as pd


class DataProcessor:
    """
    Public data processing class containing generic cleaning and validation functions.
    These functions handle common data processing tasks without exposing business logic.
    """

    @staticmethod
    def standardise_timestamp(timestamp: Union[str, datetime]) -> datetime:
        """
        Converts timestamp to UTC and standardises format.

        Args:
            timestamp: Input timestamp as string or datetime object

        Returns:
            datetime: Standardised UTC timestamp
        """
        if isinstance(timestamp, str):
            try:
                timestamp = pd.to_datetime(timestamp)
            except ValueError as e:
                raise ValueError(f"Invalid timestamp format: {e}")

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        return timestamp.astimezone(timezone.utc)

    @staticmethod
    def extract_time_features(timestamp: datetime) -> Dict[str, Any]:
        """
        Extracts useful time features from timestamp.

        Args:
            timestamp: Input datetime object

        Returns:
            dict: Dictionary containing extracted time features
        """
        return {
            "hour": timestamp.hour,
            "day_of_week": timestamp.weekday(),
            "day_of_month": timestamp.day,
            "month": timestamp.month,
            "quarter": (timestamp.month - 1) // 3 + 1,
            "year": timestamp.year,
            "is_weekend": timestamp.weekday() >= 5,
            "is_business_hours": 9 <= timestamp.hour <= 17,
        }

    @staticmethod
    def validate_coordinates(lat: float, lon: float) -> bool:
        """
        Validates geographic coordinates.

        Args:
            lat: Latitude value
            lon: Longitude value

        Returns:
            bool: True if coordinates are valid
        """
        try:
            lat = float(lat)
            lon = float(lon)
            return -90 <= lat <= 90 and -180 <= lon <= 180
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_currency_amount(amount: Union[str, float, int]) -> Optional[float]:
        """
        Validates and standardises currency amounts.

        Args:
            amount: Input amount as string or number

        Returns:
            float: Standardised amount or None if invalid
        """
        try:
            amount = float(str(amount).replace(",", ""))
            # Round to 2 decimal places for currency
            return round(amount, 2)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: list) -> bool:
        """
        Checks if all required fields are present and non-null.

        Args:
            data: Dictionary containing data fields
            required_fields: List of required field names

        Returns:
            bool: True if all required fields are present and non-null
        """
        return all(
            field in data and data[field] is not None for field in required_fields
        )

    @staticmethod
    def standardise_payment_type(payment_type: str) -> str:
        """
        Standardises payment type strings to consistent categories.

        Args:
            payment_type: Input payment type string

        Returns:
            str: Standardised payment type (CASH, CARD, or OTHER)
        """
        payment_type = str(payment_type).upper().strip()

        # Define mapping of various payment types to standard categories
        card_indicators = {"CARD", "POS", "CONTACTLESS", "VISA", "MASTERCARD", "AMEX"}
        cash_indicators = {"CASH"}

        if payment_type in cash_indicators or any(
            cash in payment_type for cash in cash_indicators
        ):
            return "CASH"
        elif payment_type in card_indicators or any(
            card in payment_type for card in card_indicators
        ):
            return "CARD"
        else:
            return "OTHER"

    @staticmethod
    def calculate_derived_amounts(
        gross_amount: float,
        vat_rate: Optional[float] = None,
        fee_rate: Optional[float] = None,
    ) -> Dict[str, float]:
        """
        Calculates derived amounts like net, VAT and fees.

        Args:
            gross_amount: Gross transaction amount
            vat_rate: Optional VAT rate as decimal
            fee_rate: Optional fee rate as decimal

        Returns:
            dict: Dictionary containing calculated amounts
        """
        results = {"gross_amount": round(gross_amount, 2)}

        if vat_rate:
            results["vat_amount"] = round(gross_amount * vat_rate / (1 + vat_rate), 2)
            results["net_amount"] = round(gross_amount - results["vat_amount"], 2)
        else:
            results["net_amount"] = results["gross_amount"]
            results["vat_amount"] = 0.0

        if fee_rate:
            results["fee_amount"] = round(results["net_amount"] * fee_rate, 2)
            results["settlement_amount"] = round(
                results["net_amount"] - results["fee_amount"], 2
            )

        return results

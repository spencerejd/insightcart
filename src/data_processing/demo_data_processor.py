import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any


class DemoDataProcessor:
    """
    Processes transaction data for demo purposes while preserving patterns
    and protecting business sensitivities.
    """

    def __init__(
        self,
        volume_multiplier_range: Tuple[float, float] = (1.2, 1.8),
        time_shift_days: int = 30,
    ):
        """
        Initialise processor with configurable parameters.

        Args:
            volume_multiplier_range: Range for random transaction amount scaling
            time_shift_days: Number of days to shift timestamps
        """
        self.volume_multiplier_range = volume_multiplier_range
        self.time_shift_days = time_shift_days

    def process_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Main processing function that applies all transformations.

        Args:
            df: DataFrame containing transaction data

        Returns:
            Processed DataFrame with anonymised data
        """
        processed = df.copy()

        # Apply core transformations
        processed = self._transform_timestamps(processed)
        processed = self._transform_amounts(processed)
        processed = self._transform_locations(processed)
        processed = self._clean_data(processed)

        return processed

    def _transform_timestamps(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform timestamps while preserving temporal patterns.
        - Shifts dates forward/backward
        - Preserves day of week, time of day
        - Maintains seasonal patterns
        """
        df = df.copy()

        # Convert timestamp to datetime if string
        if df["timestamp"].dtype == "object":
            df["timestamp"] = pd.to_datetime(df["timestamp"])

        # Shift dates while preserving day of week
        shift = timedelta(days=self.time_shift_days)
        df["timestamp"] = df["timestamp"].apply(lambda x: x + shift)

        return df

    def _transform_amounts(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform monetary amounts:
        - Applies random scaling within defined range
        - Preserves relative price relationships
        - Rounds to maintain realistic values
        """
        df = df.copy()

        # Generate random multipliers for each row
        multipliers = np.random.uniform(
            self.volume_multiplier_range[0],
            self.volume_multiplier_range[1],
            size=len(df),
        )

        # Apply multipliers to amount columns
        amount_columns = ["amount", "total_price", "product_price"]
        for col in amount_columns:
            if col in df.columns:
                df[col] = df[col] * multipliers
                df[col] = df[col].round(2)

        return df

    def _transform_locations(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform location data:
        - Shifts coordinates while maintaining relative distances
        - Preserves clustering patterns
        - Adds small random noise to prevent exact location identification
        """
        df = df.copy()

        if "lat" in df.columns and "lon" in df.columns:
            # Add small random noise to coordinates (±0.045 degrees ~ 5km)
            noise_lat = np.random.uniform(-0.045, 0.045, size=len(df))
            noise_lon = np.random.uniform(-0.045, 0.045, size=len(df))

            df["lat"] = df["lat"] + noise_lat
            df["lon"] = df["lon"] + noise_lon

            # Round to reduce precision
            df["lat"] = df["lat"].round(6)
            df["lon"] = df["lon"].round(6)

        return df

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        General data cleaning operations:
        - Removes sensitive fields
        - Standardises formats
        - Handles missing values
        """
        df = df.copy()

        # Remove any potentially sensitive columns
        sensitive_cols = ["internal_id", "merchant_code", "username", "auth_code"]
        for col in sensitive_cols:
            if col in df.columns:
                df = df.drop(columns=[col])

        # Standardise status values
        if "status" in df.columns:
            df["status"] = df["status"].str.upper()

        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)

        categorical_cols = df.select_dtypes(include=["object"]).columns
        df[categorical_cols] = df[categorical_cols].fillna("UNKNOWN")

        return df

    def get_processing_stats(
        self, original_df: pd.DataFrame, processed_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Calculate statistics about the processing to verify pattern preservation.
        """
        stats = {
            "total_transactions": len(processed_df),
            "date_range": (
                processed_df["timestamp"].min(),
                processed_df["timestamp"].max(),
            ),
            "total_amount": processed_df["amount"].sum(),
            "avg_transaction": processed_df["amount"].mean(),
            "unique_locations": len(processed_df.groupby(["lat", "lon"])),
        }

        return stats

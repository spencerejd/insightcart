"""
Enhanced DataLoader module with plotting capabilities for InsightCart Analytics.
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Dict, Any


class DataLoader:
    """Handle data loading, preprocessing and plotting operations."""

    def __init__(self, file_path: str):
        """Initialize DataLoader with file path."""
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")

        # Load data on initialization
        self.df, self.products_df = self._load_data()

    def _load_data(self) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """Load and preprocess data from JSON file."""
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
            df = pd.DataFrame(data)

            # Handle timestamp conversion
            df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601")

            # Extract product information
            df["products_list"] = df.apply(
                lambda x: x["products"] if "products" in x else [], axis=1
            )
            df["total_items"] = df.apply(
                lambda x: sum([p.get("quantity", 0) for p in x["products_list"]]),
                axis=1,
            )

            # Create products DataFrame
            products_df = self._create_products_dataframe(df)

            return df, products_df

        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return None, None

    @staticmethod
    def _get_product_price(product: Dict[str, Any]) -> float:
        """Extract product price handling different possible field names."""
        for price_field in ["price", "price_with_vat", "unit_price"]:
            if price_field in product:
                return float(product[price_field])
        return 0.0

    def _create_products_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create a separate DataFrame for product-level analysis."""
        products_data = []
        for _, row in df.iterrows():
            for product in row["products_list"]:
                product_data = {
                    "transaction_id": row["id"],
                    "timestamp": row["timestamp"],
                    "product_name": product.get("name", "Unknown"),
                    "quantity": product.get("quantity", 1),
                    "unit_price": self._get_product_price(product),
                    "total_price": product.get("total_price", 0.0),
                }
                products_data.append(product_data)
        return pd.DataFrame(products_data)

    # Financial Analytics plots
    def plot_revenue_trend(self) -> go.Figure:
        """Create daily revenue trend plot."""
        daily_revenue = (
            self.df[self.df["status"] == "SUCCESSFUL"]
            .groupby(self.df["timestamp"].dt.date)["amount"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            daily_revenue,
            x="timestamp",
            y="amount",
            title="Daily Revenue Trend",
            labels={"timestamp": "Date", "amount": "Revenue (£)"},
        )
        return fig

    def plot_payment_distribution(self) -> go.Figure:
        """Create payment method distribution plot."""
        payment_dist = self.df["payment_type"].value_counts()
        fig = px.pie(
            values=payment_dist.values,
            names=payment_dist.index,
            title="Payment Method Distribution",
        )
        return fig

    # Product Analytics plots
    def plot_top_products(self, metric: str = "quantity") -> go.Figure:
        """Create top products plot by specified metric."""
        product_sales = (
            self.products_df.groupby("product_name")
            .agg({"quantity": "sum", "total_price": "sum"})
            .reset_index()
        )

        title = f"Top 10 Products by {'Quantity Sold' if metric == 'quantity' else 'Revenue'}"
        fig = px.bar(
            product_sales.nlargest(10, metric), x="product_name", y=metric, title=title
        )
        return fig

    # Location Analytics plots
    def plot_location_map(self) -> go.Figure:
        """Create transaction locations map."""
        fig = px.scatter_mapbox(
            self.df,
            lat="lat",
            lon="lon",
            size="amount",
            color="status",
            hover_name="id",
            hover_data=["amount", "payment_type"],
            title="Transaction Locations",
            mapbox_style="carto-positron",
        )
        return fig

    # Time Analytics plots
    def plot_hourly_distribution(self) -> go.Figure:
        """Create hourly transaction distribution plot."""
        hourly_dist = self.df["timestamp"].dt.hour.value_counts().sort_index()
        fig = px.bar(
            x=hourly_dist.index,
            y=hourly_dist.values,
            title="Hourly Transaction Distribution",
            labels={"x": "Hour of Day", "y": "Number of Transactions"},
        )
        return fig

    def plot_daily_distribution(self) -> go.Figure:
        """Create daily transaction distribution plot."""
        day_mapping = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }
        self.df["day_name"] = self.df["timestamp"].dt.dayofweek.map(day_mapping)
        daily_dist = self.df["day_name"].value_counts()

        fig = px.bar(
            x=daily_dist.index,
            y=daily_dist.values,
            title="Daily Transaction Distribution",
            labels={"x": "Day of Week", "y": "Number of Transactions"},
        )
        return fig

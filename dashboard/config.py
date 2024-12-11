"""
Configuration module for InsightCart Analytics.
Handles command-line arguments and application settings.
"""

import argparse
from pathlib import Path
import streamlit as st
from typing import Optional


class Config:
    _instance = None
    _initialised = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not Config._initialised:
            self.data_path: Optional[Path] = None
            Config._initialised = True

    @classmethod
    def initialise(cls):
        """Initialise configuration from command line arguments."""
        parser = argparse.ArgumentParser(description="InsightCart Analytics Dashboard")
        parser.add_argument(
            "--data-path", type=str, required=False, help="Path to the JSON data file"
        )

        # Parse args only if they haven't been parsed (handles Streamlit's double run)
        if not cls._instance or not cls._instance.data_path:
            try:
                # Try to parse arguments, ignoring unknown args (for Streamlit Cloud)
                args, _ = parser.parse_known_args()
                instance = cls()

                if args.data_path:
                    # If data path is provided via command line
                    instance.data_path = Path(args.data_path)
                else:
                    # Default path for cloud deployment
                    default_path = (
                        Path(__file__).parent / "data" / "demo_transactions.json"
                    )
                    instance.data_path = default_path

                # Validate the data path
                if not instance.data_path.exists():
                    raise FileNotFoundError(
                        f"Data file not found: {instance.data_path}\n"
                        f"Please ensure the file exists at the specified location."
                    )
                if not instance.data_path.suffix.lower() == ".json":
                    raise ValueError("Data file must be a JSON file")

            except SystemExit:
                # Handle the case when running in Streamlit Cloud
                default_path = Path(__file__).parent / "data" / "demo_transactions.json"
                instance = cls()
                instance.data_path = default_path

                if not instance.data_path.exists():
                    st.error(
                        """
                    Please ensure data file exists at one of these locations:
                    1. Provided path (local development):
                       streamlit run Home.py -- --data-path path/to/your/data.json
                    2. Default path (cloud deployment):
                       dashboard/data/demo_transactions.json
                    """
                    )
                    return None

        return cls._instance

    @classmethod
    def get_instance(cls):
        """Get the singleton instance of Config."""
        if not cls._instance:
            cls._instance = cls.initialise()
        return cls._instance

"""
This module provides operations for interacting with Supabase,
including authentication, data fetching, insertion, and upsertion.
"""

import os
import json
from supabase import create_client, Client
from typing import Dict, List, Any
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SupabaseOperations:
    """
    This class provides methods to interact with Supabase, including
    authentication, data fetching, insertion, and upsertion.
    """

    def __init__(self):
        """Initialize Supabase client with credentials from environment variables."""
        # Load environment variables
        load_dotenv()

        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("SUPABASE_KEY")
        self.user_email: str = os.environ.get("SUPABASE_USER_EMAIL")
        self.user_password: str = os.environ.get("SUPABASE_USER_PASSWORD")

        if not all([self.url, self.key, self.user_email, self.user_password]):
            raise ValueError(
                "SUPABASE_URL, SUPABASE_KEY, SUPABASE_USER_EMAIL and SUPABASE_USER_PASSWORD must be set in environment variables"
            )

        self.supabase: Client = create_client(self.url, self.key)
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with Supabase using email and password."""
        try:
            response = self.supabase.auth.sign_in_with_password(
                {"email": self.user_email, "password": self.user_password}
            )
            logger.info("Successfully authenticated with Supabase")
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise

    def test_connection(self) -> bool:
        """Test the connection to Supabase."""
        try:
            response = (
                self.supabase.table("transactions").select("*").limit(1).execute()
            )
            logger.info("Successfully connected to Supabase")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Supabase: {str(e)}")
            return False

    def fetch_transactions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch transactions from Supabase.

        Args:
            limit (int): Maximum number of records to fetch
        """
        try:
            response = (
                self.supabase.table("transactions").select("*").limit(limit).execute()
            )
            transactions = response.data
            logger.info(f"Successfully fetched {len(transactions)} transactions")
            return transactions
        except Exception as e:
            logger.error(f"Error fetching transactions: {str(e)}")
            return []

    def insert_data(self, file_path: str) -> bool:
        """
        Insert data from a JSON file into Supabase.

        Args:
            file_path (str): Path to the JSON file containing data to insert
        """
        try:
            with open(file_path, "r") as file:
                data = json.load(file)

            if not isinstance(data, list):
                data = [data]  # Convert single object to list

            response = self.supabase.table("products").insert(data).execute()
            logger.info(f"Successfully inserted {len(data)} records")
            return True
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return False
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON file: {file_path}")
            return False
        except Exception as e:
            logger.error(f"Error inserting data: {str(e)}")
            return False

    def upsert_data(self, file_path: str) -> bool:
        """
        Upsert data from a JSON file into Supabase.

        Args:
            file_path (str): Path to the JSON file containing data to upsert
        """
        try:
            with open(file_path, "r") as file:
                data = json.load(file)

            if not isinstance(data, list):
                data = [data]  # Convert single object to list

            response = self.supabase.table("products").upsert(data).execute()
            logger.info(f"Successfully upserted {len(data)} records")
            return True
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return False
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON file: {file_path}")
            return False
        except Exception as e:
            logger.error(f"Error upserting data: {str(e)}")
            return False


def main():
    """Main function to run all Supabase operations."""
    try:
        # Initialize Supabase operations
        supabase_ops = SupabaseOperations()

        # Test connection
        if not supabase_ops.test_connection():
            logger.error("Exiting due to connection failure")
            return

        # Fetch transactions
        transactions = supabase_ops.fetch_transactions(limit=10)
        if transactions:
            logger.info(f"First transaction: {transactions[0]}")

        # Insert data
        insert_path = "output_directory/products.json"
        if supabase_ops.insert_data(insert_path):
            logger.info("Insert operation completed successfully")

        # Upsert data
        upsert_path = "output_directory/products.json"
        if supabase_ops.upsert_data(upsert_path):
            logger.info("Upsert operation completed successfully")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()

import json
import argparse
from pathlib import Path
from datetime import datetime
import pandas as pd
from config.demo_mappings import demo_mapping
from src.data_processing.demo_data_processor import DemoDataProcessor


def load_sumup_data(json_file: str) -> pd.DataFrame:
    """
    Load and preprocess SumUp JSON data into a pandas DataFrame.
    """
    # Validate file exists
    if not Path(json_file).exists():
        raise FileNotFoundError(f"Could not find JSON file: {json_file}")

    # Read JSON file
    with open(json_file, "r") as f:
        data = json.load(f)

    # Extract main transaction data
    transactions = []
    for transaction in data:
        # Basic transaction info
        trans_dict = {
            "id": transaction["id"],
            "timestamp": transaction["timestamp"],
            "amount": transaction["amount"],
            "currency": transaction["currency"],
            "status": transaction["status"],
            "payment_type": transaction["payment_type"],
            "lat": transaction["location"]["lat"],
            "lon": transaction["location"]["lon"],
        }

        # Extract product information
        products = transaction.get("products", [])
        if products:
            # Take the first product for simplicity in this example
            product = products[0]
            trans_dict.update(
                {
                    "product_name": product.get("name", ""),
                    "product_price": product.get("price", 0.0),
                    "product_quantity": product.get("quantity", 1),
                    "total_price": product.get("total_price", 0.0),
                }
            )

        transactions.append(trans_dict)

    return pd.DataFrame(transactions)


def apply_demo_mappings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply demo product name mappings while preserving the DataFrame structure.
    Includes proper string cleaning to ensure consistent mapping.
    """
    df = df.copy()

    # Keep original for verification
    df["original_product_name"] = df["product_name"]

    # Clean product names before mapping:
    # 1. Strip whitespace
    # 2. Handle case consistency
    df["product_name"] = df["product_name"].str.strip()

    # Apply mapping with better fallback handling
    def map_product(product_name):
        # Try exact match first
        if product_name in demo_mapping:
            return demo_mapping[product_name]

        # If no match, try case-insensitive match
        for original, mapped in demo_mapping.items():
            if original.lower() == product_name.lower():
                return mapped

        # If still no match, log it for debugging
        print(f"Warning: No mapping found for product: '{product_name}'")
        return "Other Product"

    df["product_name"] = df["product_name"].apply(map_product)

    # Add debugging information
    unique_products = df["original_product_name"].unique()
    print("\nUnique products in input data:")
    for product in sorted(unique_products):
        mapped_name = map_product(product.strip())
        print(f"'{product}' -> '{mapped_name}'")

    return df


def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="Process SumUp transaction data for demo purposes"
    )
    parser.add_argument(
        "input_file", help="Path to input JSON file containing SumUp transactions"
    )
    parser.add_argument(
        "--output-file",
        "-o",
        help="Path to output CSV file (default: demo_processed_transactions.csv)",
        default="demo_processed_transactions.csv",
    )
    parser.add_argument(
        "--volume-min",
        type=float,
        default=1.3,
        help="Minimum volume multiplier (default: 1.3)",
    )
    parser.add_argument(
        "--volume-max",
        type=float,
        default=1.7,
        help="Maximum volume multiplier (default: 1.7)",
    )
    parser.add_argument(
        "--time-shift",
        type=int,
        default=45,
        help="Number of days to shift timestamps (default: 45)",
    )

    args = parser.parse_args()

    # Initialize our demo processor with command line parameters
    processor = DemoDataProcessor(
        volume_multiplier_range=(args.volume_min, args.volume_max),
        time_shift_days=args.time_shift,
    )

    # Load and preprocess the data
    print(f"Loading SumUp data from {args.input_file}...")
    try:
        df = load_sumup_data(args.input_file)
        print(f"Loaded {len(df)} transactions")
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return

    # Apply demo mappings
    print("\nApplying product mappings...")
    df = apply_demo_mappings(df)

    # Process the data
    print("\nProcessing transactions...")
    processed_df = processor.process_transactions(df)

    # Print sample of original vs processed data
    print("\nSample Comparison (First Transaction):")
    comparison_cols = ["timestamp", "amount", "product_name", "total_price"]
    print("\nOriginal:")
    print(df[comparison_cols].iloc[0])
    print("\nProcessed:")
    print(processed_df[comparison_cols].iloc[0])

    # Get and print processing statistics
    print("\nProcessing Statistics:")
    stats = processor.get_processing_stats(df, processed_df)
    for key, value in stats.items():
        print(f"{key}: {value}")

    # Verify data anonymisation
    print("\nVerifying Anonymisation:")
    print(f"Original date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(
        f"Processed date range: {processed_df['timestamp'].min()} to {processed_df['timestamp'].max()}"
    )
    print(f"\nUnique original products: {df['original_product_name'].nunique()}")
    print(f"Unique mapped products: {processed_df['product_name'].nunique()}")

    # Save processed data to CSV for verification
    try:
        processed_df.to_csv(args.output_file, index=False)
        print(f"\nProcessed data saved to {args.output_file}")
    except Exception as e:
        print(f"Error saving output file: {str(e)}")


if __name__ == "__main__":
    main()

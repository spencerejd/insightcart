import streamlit as st
from pathlib import Path
from typing import Optional, Tuple

class ImageHelper:
    """Helper class for managing images in Streamlit pages"""
    
    @staticmethod
    def display_hero_image(image_path: str, width: Optional[int] = None) -> None:
        """Display a hero/banner image at the top of the page"""
        try:
            st.image(image_path, width=width, use_column_width=width is None)
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")

    @staticmethod
    def create_image_columns(
        image_paths: list,
        widths: Optional[list] = None,
        captions: Optional[list] = None
    ) -> None:
        """Create columns with images"""
        cols = st.columns(len(image_paths))
        for idx, col in enumerate(cols):
            with col:
                try:
                    width = widths[idx] if widths else None
                    caption = captions[idx] if captions else None
                    col.image(
                        image_paths[idx],
                        width=width,
                        use_column_width=width is None,
                        caption=caption
                    )
                except Exception as e:
                    col.error(f"Error loading image {idx + 1}: {str(e)}")

# Usage examples for each page:

def update_home_page():
    """Add market scene image to home page"""
    # After the title section in Home.py
    ImageHelper.display_hero_image(
        "path/to/market_payment.jpg",  # Image 1
        width=800  # Full width for hero image
    )

def update_financial_page():
    """Add payment terminal image to financial analytics"""
    # After the title in 1_Financial_Analytics.py
    ImageHelper.display_hero_image(
        "path/to/card_payment.jpg",  # Image 2
        width=700  # Slightly smaller for section header
    )

def update_product_page():
    """Add pastry image to product analytics"""
    # After the title in 2_Product_Analytics.py
    ImageHelper.display_hero_image(
        "path/to/pastries.jpg",  # Image 3
        width=700  # Consistent with financial page
    )

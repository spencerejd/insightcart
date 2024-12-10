import streamlit as st
from pathlib import Path
from dashboard.data_loader import DataLoader
from dashboard.config import Config

st.set_page_config(page_title="InsightCart Analytics", page_icon="🛍️", layout="wide")


def main():
    # Initialise configuration
    config = Config.get_instance()
    if not config or not config.data_path:
        st.error("Please configure the application with valid data path")
        return

    # Initialise DataLoader with config path
    try:
        loader = DataLoader(config.data_path)

        # Header section with logo and title
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://via.placeholder.com/150", width=150)
        with col2:
            st.title("InsightCart Analytics")
            st.subheader("Mobile Market Analytics Made Simple")

        # Introduction section
        st.markdown(
            """
        ### Transform Your Mobile Market Data into Actionable Insights
        
        InsightCart seamlessly integrates POS data for mobile market retailers across the UK, 
        providing real-time analytics and insights to drive business growth. Whether you're 
        selling at farmers' markets, food festivals, or pop-up locations, we help you understand 
        your business better.
        """
        )

        # Key Features section with icons
        st.markdown("### Key Features")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("#### 📊 Financial Analytics")
            st.markdown(
                "Track revenue trends, payment methods, and transaction patterns across all your locations."
            )

        with col2:
            st.markdown("#### 📦 Product Analytics")
            st.markdown(
                "Identify your best-selling products and understand performance across different markets."
            )

        with col3:
            st.markdown("#### 🗺️ Location Analytics")
            st.markdown(
                "Visualise your market presence and performance across different locations."
            )

        with col4:
            st.markdown("#### ⏰ Time Analytics")
            st.markdown(
                "Understand peak trading hours and optimise your schedule for maximum revenue."
            )

        # Getting Started section
        st.markdown("### Getting Started")
        st.markdown(
            """
        Navigate through the different analytics pages using the sidebar menu to explore your data:

        1. **Financial Analytics**: Review your revenue trends and payment patterns
        2. **Product Analytics**: Analyse product performance and inventory insights
        3. **Location Analytics**: Explore geographical performance data
        4. **Time Analytics**: Understand temporal patterns in your sales

        Each page provides detailed visualisations and insights specific to that aspect of your business.
        """
        )

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return


if __name__ == "__main__":
    main()

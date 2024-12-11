import streamlit as st
import pygwalker as pyg
import pandas as pd
from dashboard.data_loader import DataLoader
from dashboard.config import Config


def render_interactive_analytics():
    # Initialise configuration
    config = Config.get_instance()
    if not config or not config.data_path:
        st.error("Please configure the application with valid data path")
        return

    try:
        # Initialise DataLoader
        loader = DataLoader(config.data_path)
        df = loader.df
        products_df = loader.products_df

        st.title("Custom Analytics")
        st.markdown(
            """
        ### Customise Key Business Metrics
        Explore your data through these pre-configured views. Each view focuses on a specific 
        aspect of your business, but you can modify the variables to suit your needs.
        """
        )

        # Create focused analysis sections
        analysis_type = st.selectbox(
            "Choose Analysis Type",
            ["Revenue Analysis", "Product Performance", "Time-of-Day Analysis"],
        )

        if analysis_type == "Revenue Analysis":
            st.markdown("### Daily Revenue Patterns")
            st.markdown(
                "Explore your revenue patterns by day, payment method, or location. Modify the chart to show the metrics that matter most to you."
            )

            # Prepare data for revenue analysis
            revenue_df = df.copy()
            revenue_df["date"] = pd.to_datetime(revenue_df["timestamp"]).dt.date
            revenue_df = (
                revenue_df.groupby(["date", "payment_type"])["amount"]
                .agg(["sum", "count"])
                .reset_index()
            )
            revenue_df.columns = [
                "Date",
                "Payment Method",
                "Total Revenue",
                "Transaction Count",
            ]

            pyg_html = pyg.to_html(
                revenue_df, use_kernel_calc=True, dark="auto", height=400
            )
            st.components.v1.html(pyg_html, height=400, scrolling=True)

        elif analysis_type == "Product Performance":
            st.markdown("### Product Sales Analysis")
            st.markdown(
                "Compare product performance across different metrics. Adjust the view to focus on quantity sold, revenue, or average transaction value."
            )

            # Prepare data for product analysis
            product_analysis = (
                products_df.groupby("product_name")
                .agg({"quantity": "sum", "total_price": "sum"})
                .reset_index()
            )
            product_analysis["average_price"] = (
                product_analysis["total_price"] / product_analysis["quantity"]
            )
            product_analysis.columns = [
                "Product",
                "Units Sold",
                "Total Revenue",
                "Average Price",
            ]

            pyg_html = pyg.to_html(
                product_analysis, use_kernel_calc=True, dark="auto", height=400
            )
            st.components.v1.html(pyg_html, height=400, scrolling=True)

        else:  # Time-of-Day Analysis
            st.markdown("### Hourly Sales Patterns")
            st.markdown(
                "Understand your peak trading hours and busy periods. Modify the view to explore different time-based patterns."
            )

            # Prepare data for time analysis
            time_df = df.copy()
            time_df["Hour"] = pd.to_datetime(time_df["timestamp"]).dt.hour
            time_df["Day of Week"] = pd.to_datetime(time_df["timestamp"]).dt.day_name()
            time_analysis = (
                time_df.groupby(["Hour", "Day of Week"])
                .agg({"amount": ["sum", "count"]})
                .reset_index()
            )
            time_analysis.columns = [
                "Hour",
                "Day of Week",
                "Total Revenue",
                "Transaction Count",
            ]

            pyg_html = pyg.to_html(
                time_analysis, use_kernel_calc=True, dark="auto", height=400
            )
            st.components.v1.html(pyg_html, height=400, scrolling=True)

        # Add helpful tips for using the current view
        with st.expander("📈 Tips for using this view"):
            st.markdown(
                """
            - Click and drag fields to change what's shown on each axis
            - Use the chart type selector to switch between different visualisations
            - Apply filters by clicking on the filter icon next to any field
            - Double-click on elements to focus on specific data points
            """
            )

    except Exception as e:
        st.error(f"Error loading interactive analytics: {str(e)}")
        return


if __name__ == "__main__":
    render_interactive_analytics()

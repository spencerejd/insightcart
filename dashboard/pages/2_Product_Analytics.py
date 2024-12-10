import streamlit as st
from dashboard.data_loader import DataLoader
from dashboard.config import Config


def render_product_analytics():
    # Initialise configuration
    config = Config.get_instance()
    if not config or not config.data_path:
        st.error("Please configure the application with valid data path")
        return

    # Initialise DataLoader
    try:
        loader = DataLoader(config.data_path)
        products_df = loader.products_df  # Get the products DataFrame

        st.title("Product Analytics")
        st.markdown(
            """
        ### Product Performance Insights
        Analyse your product portfolio performance across different markets and time periods. 
        Identify top sellers and optimise your inventory based on real data.
        """
        )

        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            total_products = len(products_df["product_name"].unique())
            st.metric("Unique Products", total_products)
        with col2:
            total_units = products_df["quantity"].sum()
            st.metric("Total Units Sold", f"{total_units:,}")
        with col3:
            total_revenue = products_df["total_price"].sum()
            st.metric("Total Product Revenue", f"£{total_revenue:,.2f}")

        # Product visualisations
        col1, col2 = st.columns(2)
        with col1:
            # Top products by quantity
            st.plotly_chart(
                loader.plot_top_products(metric="quantity"), use_container_width=True
            )

        with col2:
            # Top products by revenue
            st.plotly_chart(
                loader.plot_top_products(metric="total_price"), use_container_width=True
            )

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return


if __name__ == "__main__":
    render_product_analytics()

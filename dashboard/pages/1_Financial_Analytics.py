import streamlit as st
from dashboard.data_loader import DataLoader
from dashboard.config import Config


def render_financial_analytics():
    # Initialise configuration
    config = Config.get_instance()
    if not config or not config.data_path:
        st.error("Please configure the application with valid data path")
        return

    # Initialise DataLoader
    try:
        loader = DataLoader(config.data_path)
        df = loader.df  # Get the main DataFrame

        st.title("Financial Analytics")
        st.markdown(
            """
        ### Understanding Your Revenue
        Track your financial performance with comprehensive analytics on revenue, 
        transaction patterns, and payment methods. Use these insights to make 
        data-driven decisions about your business operations.
        """
        )

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Revenue", f"£{df['amount'].sum():.2f}")
        with col2:
            st.metric("Average Transaction", f"£{df['amount'].mean():.2f}")
        with col3:
            st.metric("Total Transactions", len(df))
        with col4:
            success_rate = (len(df[df["status"] == "SUCCESSFUL"]) / len(df)) * 100
            st.metric("Success Rate", f"{success_rate:.1f}%")

        # Revenue trend plot
        st.plotly_chart(loader.plot_revenue_trend(), use_container_width=True)

        # Payment method distribution plot
        st.plotly_chart(loader.plot_payment_distribution(), use_container_width=True)

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return


if __name__ == "__main__":
    render_financial_analytics()

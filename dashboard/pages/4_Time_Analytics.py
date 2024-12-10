import streamlit as st
from dashboard.data_loader import DataLoader
from dashboard.config import Config


def render_time_analytics():
    # Initialise configuration
    config = Config.get_instance()
    if not config or not config.data_path:
        st.error("Please configure the application with valid data path")
        return

    # Initialise DataLoader
    try:
        loader = DataLoader(config.data_path)
        df = loader.df  # Get the main DataFrame

        st.title("Time Analytics")
        st.markdown(
            """
        ### Temporal Pattern Analysis
        Discover patterns in your trading hours and days. Use these insights to 
        optimise your schedule and maximise revenue during peak times.
        """
        )

        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            busiest_hour = df["timestamp"].dt.hour.mode().iloc[0]
            st.metric("Busiest Hour", f"{busiest_hour:02d}:00")
        with col2:
            busiest_day = df["timestamp"].dt.day_name().mode().iloc[0]
            st.metric("Busiest Day", busiest_day)
        with col3:
            avg_daily_transactions = len(df) / df["timestamp"].dt.date.nunique()
            st.metric("Avg Daily Transactions", f"{avg_daily_transactions:.1f}")

        # Time distribution visualisations
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(loader.plot_hourly_distribution(), use_container_width=True)
        with col2:
            st.plotly_chart(loader.plot_daily_distribution(), use_container_width=True)

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return


if __name__ == "__main__":
    render_time_analytics()

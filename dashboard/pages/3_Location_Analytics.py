import streamlit as st
from dashboard.data_loader import DataLoader
from dashboard.config import Config


def render_location_analytics():
    # Initialise configuration
    config = Config.get_instance()
    if not config or not config.data_path:
        st.error("Please configure the application with valid data path")
        return

    # Initialise DataLoader
    try:
        loader = DataLoader(config.data_path)
        df = loader.df  # Get the main DataFrame

        st.title("Location Analytics")
        st.markdown(
            """
        ### Geographical Performance Analysis
        Visualise your market presence and performance across different locations. 
        Understand which markets work best for your business and optimise your route planning.
        """
        )

        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            unique_locations = df.groupby(["lat", "lon"]).size().shape[0]
            st.metric("Unique Locations", unique_locations)
        with col2:
            avg_per_location = df.groupby(["lat", "lon"])["amount"].mean().mean()
            st.metric("Average Revenue per Location", f"£{avg_per_location:.2f}")
        with col3:
            most_visited = df.groupby(["lat", "lon"]).size().max()
            st.metric("Most Visits to Single Location", most_visited)

        # Location map
        st.plotly_chart(loader.plot_location_map(), use_container_width=True)

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return


if __name__ == "__main__":
    render_location_analytics()

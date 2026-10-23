"""
LifeLine Navigator — Emergency Map Page
Final version with robust error handling
"""
import streamlit as st
from src.ui import init_page, init_sidebar
from src.config import MAP_CENTER

# Ensure map libraries are imported at module level
try:
    import folium
    from streamlit_folium import st_folium
    from folium.plugins import AntPath
    from src.ui.components import create_base_map, add_route_line
    from src.api.schemas import Coordinates
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

def render_map_page():
    """Render emergency map page with comprehensive error handling"""
    # Initialize page
    init_page("LifeLine Navigator — Emergency Map")
    init_sidebar()

    # Header
    st.title("🗺️ Emergency Map")
    st.write("Real-time hazards • Safe routing • Family coordination")

    # Emergency contacts
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.button("📞 112", use_container_width=True)
    with col2: st.button("🔥 101", use_container_width=True)
    with col3: st.button("🚑 102/108", use_container_width=True)
    with col4: st.button("👮 100", use_container_width=True)

    # Main content
    try:
        # Check if folium is available
        if not FOLIUM_AVAILABLE:
            raise ImportError("folium library not available")

        # Map loaded successfully

        # Create map using base map components
        m = create_base_map(MAP_CENTER)

        # Add dark theme filter
        folium.Element(
            """
            <style>
            .leaflet-tile-pane {
                filter: brightness(0.6) invert(1) hue-rotate(180deg) saturate(0.3);
            }
            </style>
            """
        ).add_to(m)

        # Add sample data
        folium.Marker(
            MAP_CENTER,
            popup="Your Location",
            icon=folium.Icon(color='blue', icon='user')
        ).add_to(m)

        folium.Circle(
            MAP_CENTER,
            radius=1000,
            color='red',
            fill=True,
            fillOpacity=0.3,
            popup="Hazard Zone"
        ).add_to(m)

        # Add routing functionality
        # Sample route data (in real app, this would be calculated)
        route_data = [
            {'latitude': MAP_CENTER[0], 'longitude': MAP_CENTER[1]},
            {'latitude': MAP_CENTER[0] + 0.01, 'longitude': MAP_CENTER[1] + 0.01},
            {'latitude': MAP_CENTER[0] + 0.02, 'longitude': MAP_CENTER[1] + 0.005}
        ]
        add_route_line(m, route_data)

        # Display map
        st_folium(m, use_container_width=True, height=620)

        # Map controls
        st.write("### Map Controls")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📍 Set My Location", use_container_width=True):
                # Update user location marker
                new_location = [MAP_CENTER[0] + 0.005, MAP_CENTER[1] + 0.005]
                folium.Marker(
                    location=new_location,
                    popup="Updated Location",
                    icon=folium.Icon(color='green', icon='user')
                ).add_to(m)

                st.toast("Location updated!")
                st.rerun()

        with col2:
            if st.button("🛣️ Calculate Route", use_container_width=True):
                # Add new route
                new_route = [
                    {'latitude': MAP_CENTER[0], 'longitude': MAP_CENTER[1]},
                    {'latitude': MAP_CENTER[0] + 0.015, 'longitude': MAP_CENTER[1] + 0.01},
                    {'latitude': MAP_CENTER[0] + 0.03, 'longitude': MAP_CENTER[1] + 0.02}
                ]

                folium.PolyLine(
                    locations=[[p['latitude'], p['longitude']] for p in new_route],
                    color='#FF8A3D',
                    weight=6,
                    opacity=0.8,
                    popup="Updated Safe Route"
                ).add_to(m)

                st.toast("Route calculated!")
                st.rerun()

        with col3:
            if st.button("🪨 Mark Debris", use_container_width=True):
                # Add debris marker at current view center (simplified)
                debris_location = [MAP_CENTER[0] + 0.01, MAP_CENTER[1] - 0.01]
                folium.Marker(
                    location=debris_location,
                    popup="Debris",
                    icon=folium.Icon(color='orange', icon='warning', prefix='fa')
                ).add_to(m)

                st.toast("Debris marked!")
                st.rerun()

        
    except ImportError as e:
        # Handle missing libraries gracefully
        st.error(f"""
        ### ❌ Map Libraries Not Available

        Error details: {str(e)}

        **To install the required packages:**
        ```bash
        pip install folium streamlit-folium
        ```

        **Alternatively, you can:**
        1. Use the other pages of the app
        2. Check back after installing the libraries
        """)

        # Show a static image or placeholder
        st.info("""
        ### 🗺️ Emergency Map Features

        When the map is working, it will show:
        - Real-time hazard zones
        - Nearby emergency shelters
        - Safe routing paths
        - Your current location
        - Family meetup points

        In the meantime, please use the navigation to access other features.
        """)

    except Exception as e:
        # Handle any other errors
        import traceback
        error_details = traceback.format_exc()

        st.error(f"""
        ### ❌ Error Loading Map

        We encountered an error while loading the map:

        ```
        {str(e)}
        ```

        **Full error details:**
        ```
        {error_details}
        ```

        Please try refreshing the page or check if all required libraries are installed.
        """)

        # Show alternative content
        st.warning("📱 For emergency assistance, call 112 or use the quick action buttons above.")


# For testing
if __name__ == "__main__":
    render_map_page()
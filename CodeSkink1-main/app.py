"""
LifeLine Navigator — Main Entry Point
Streamlit multi-page application for emergency navigation.
Run: streamlit run app.py
"""
import streamlit as st
from src.ui.pages import (
    render_home, render_map_page,
    render_family_page, render_alerts_page, render_settings_page
)


# ──────────────────────────────────────────────
# PAGE ROUTING
# ──────────────────────────────────────────────
PAGES = {
    "home": render_home,
    "map_page": render_map_page,
    "family_page": render_family_page,
    "alerts_page": render_alerts_page,
    "settings_page": render_settings_page,
}


def main():
    """Main application entry point."""
    # Configure Streamlit - MUST be called first
    st.set_page_config(
        layout="wide",
        page_title="LifeLine Navigator",
        page_icon="🚨",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    # Get current page renderer
    page_key = st.session_state.current_page
    render_func = PAGES.get(page_key, render_home)

    # Render page
    try:
        render_func()
    except Exception as e:
        st.error(f"Error rendering page: {e}")
        if st.button("🏠 Go Home"):
            st.session_state.current_page = "home"
            st.rerun()


if __name__ == "__main__":
    main()
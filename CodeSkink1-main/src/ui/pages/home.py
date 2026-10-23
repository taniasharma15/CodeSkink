"""
LifeLine Navigator — Home Page
Professional dashboard with hero section and emergency quick actions.
"""
import streamlit as st
import textwrap
from src.ui import (
    init_page, init_sidebar, render_emergency_title, render_page_title,
    render_section_title, render_metric_card, render_status_badge,
    render_offline_badge, render_emergency_contacts
)
from src.ui.components import (
    hazard_card, shelter_card, render_empty_hazards, render_empty_shelters,
    create_base_map, add_shelter_markers, render_live_status
)
from src.api import get_app_service, get_shelter_service, get_hazard_service
from src.api.schemas import ShelterSearchRequest, Coordinates
from src.config import MAP_CENTER, HAZARD_ICONS, SHELTER_TYPES


def render_home():
    """Render home dashboard with professional layout."""
    init_page("LifeLine Navigator — Home")
    init_sidebar()

    # Hero Section
    hero_html = textwrap.dedent("""
        <div style="text-align: center; padding: var(--spacing-2xl) 0; margin-bottom: var(--spacing-2xl);">
            <h1 style="font-size: 48px; font-weight: 800; margin-bottom: var(--spacing-lg);
                       background: linear-gradient(135deg, #FF4D4F 0%, #FF8A3D 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       animation: shimmer 3s infinite;">
                Navigate safely when every second counts
            </h1>
            <p style="font-size: 20px; color: var(--text-secondary); margin-bottom: var(--spacing-2xl);">
                Offline-first emergency navigation system for Amritsar
            </p>
        </div>
    """)
    st.markdown(hero_html, unsafe_allow_html=True)

    # Quick Action Buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🗺️ Open Emergency Map", use_container_width=True, key="btn_map"):
            st.session_state.current_page = "map_page"
            st.rerun()
    with col2:
        if st.button("👨‍👩‍👧‍👦 Family Tracker", use_container_width=True, key="btn_family"):
            st.session_state.current_page = "family_page"
            st.rerun()
    with col3:
        if st.button("🔔 Test Alerts", use_container_width=True, key="btn_alerts"):
            st.session_state.current_page = "alerts_page"
            st.rerun()

    # Emergency Contacts
    st.markdown("<div style='margin-bottom: var(--spacing-2xl);'></div>", unsafe_allow_html=True)
    render_emergency_contacts()

    st.divider()

    # Services
    app_service = get_app_service()
    shelter_service = get_shelter_service()
    hazard_service = get_hazard_service()

    status = app_service.get_status()
    hazards = hazard_service.get_active_hazards()

    # Store hazard counts for sidebar
    hazard_counts = {}
    for h in hazards:
        hazard_counts[h.type.value] = hazard_counts.get(h.type.value, 0) + 1
    st.session_state.active_hazard_counts = hazard_counts

    # Key Metrics Row
    render_section_title("System Overview")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    with kpi_col1:
        render_metric_card("Shelters Loaded", str(status.shelters_loaded), status="safe")
    with kpi_col2:
        render_metric_card("Active Hazards", str(status.hazards_active), status="active" if status.hazards_active > 0 else "safe")
    with kpi_col3:
        render_metric_card("Offline Mode", "Enabled", status="safe")
    with kpi_col4:
        render_metric_card("API Status", "Connected" if status.api_connected else "Offline",
                          status="safe" if status.api_connected else "warning")

    st.divider()

    # Active Hazards Section
    render_section_title("🚨 Active Hazards")
    if not hazards:
        render_empty_hazards()
    else:
        # Filter chips
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("All Types", use_container_width=True):
                pass  # Filter logic would go here
        with col2:
            if st.button("Critical Only", use_container_width=True):
                pass  # Filter logic would go here
        with col3:
            if st.button("Recent", use_container_width=True):
                pass  # Filter logic would go here

        st.markdown("<div style='margin-bottom: var(--spacing-md);'></div>", unsafe_allow_html=True)

        # Hazard Cards Grid
        hazard_col1, hazard_col2 = st.columns(2)
        for i, hazard in enumerate(hazards[:4]):  # Show first 4
            with hazard_col1 if i % 2 == 0 else hazard_col2:
                st.markdown(hazard_card(hazard), unsafe_allow_html=True)

        if len(hazards) > 4:
            st.markdown(f"""
            <div style="text-align: center; margin-top: var(--spacing-md);">
                <a style="color: var(--info); text-decoration: none; font-size: var(--font-size-sm);">
                    + {len(hazards) - 4} more hazards
                </a>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Nearby Shelters Section
    render_section_title("🏠 Nearby Emergency Shelters")

    # Get nearby shelters
    shelters_request = ShelterSearchRequest(
        location=Coordinates(latitude=31.6200, longitude=74.8765),  # Golden Temple area
        radius_km=5,
        min_capacity=0,
        shelter_types=None,
        limit=6
    )
    nearby_shelters = shelter_service.search_shelters(shelters_request)

    if not nearby_shelters:
        render_empty_shelters()
    else:
        # Shelter Cards Grid
        shelter_col1, shelter_col2, shelter_col3 = st.columns(3)
        for i, shelter in enumerate(nearby_shelters[:6]):
            with shelter_col1 if i % 3 == 0 else shelter_col2 if i % 3 == 1 else shelter_col3:
                # Render shelter card
                st.markdown(shelter_card(shelter), unsafe_allow_html=True)

    st.divider()

    # How LifeLine Works Section
    render_section_title("🚀 How LifeLine Works")
    steps_html = textwrap.dedent("""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: var(--spacing-xl);">
            <div class="glass-card" style="text-align: center; padding: var(--spacing-xl);">
                <span style="font-size: 48px;">🔍</span>
                <h3 style="margin: var(--spacing-md) 0; font-weight: 700;">Detect</h3>
                <p style="color: var(--text-secondary); margin: 0;">
                    Monitor hazards in real-time and get instant alerts
                </p>
            </div>
            <div class="glass-card" style="text-align: center; padding: var(--spacing-xl);">
                <span style="font-size: 48px;">🛣️</span>
                <h3 style="margin: var(--spacing-md) 0; font-weight: 700;">Route</h3>
                <p style="color: var(--text-secondary); margin: 0;">
                    Calculate safe paths avoiding danger zones
                </p>
            </div>
            <div class="glass-card" style="text-align: center; padding: var(--spacing-xl);">
                <span style="font-size: 48px;">👥</span>
                <h3 style="margin: var(--spacing-md) 0; font-weight: 700;">Reunite</h3>
                <p style="color: var(--text-secondary); margin: 0;">
                    Coordinate with family and find meetup points
                </p>
            </div>
        </div>
    """)
    st.markdown(steps_html, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: var(--spacing-2xl); padding: var(--spacing-xl);
                 border-top: 1px solid var(--border); color: var(--text-secondary);">
        <p style="margin: 0; font-size: var(--font-size-sm);">
            Built for Amritsar • Offline-first • v1.0
        </p>
    </div>
    """, unsafe_allow_html=True)
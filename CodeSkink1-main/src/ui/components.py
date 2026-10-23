"""
LifeLine Navigator — Reusable UI Components
Professional emergency navigation components with dark theme.
"""
import streamlit as st
from typing import List, Dict, Optional, Callable, Any
from datetime import datetime

# Map libraries for components
try:
    import folium
    from folium.plugins import AntPath
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False
from src.ui.styles import (
    inject_main_css, render_emergency_title, render_page_title,
    render_section_title, render_status_badge, render_metric_card,
    render_hazard_legend, render_offline_badge, render_live_status,
    render_emergency_contacts, dedent_html
)
from src.api.schemas import Shelter, Hazard, FamilyMember, Coordinates
from src.config import HAZARD_COLORS, HAZARD_ICONS, SHELTER_TYPES

# ──────────────────────────────────────────────
# INITIALIZATION
# ──────────────────────────────────────────────
def init_page(page_title: str = "LifeLine Navigator"):
    """Initialize page with styles and config."""
    inject_main_css()
    render_live_status()

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
def init_sidebar():
    """Initialize sidebar with navigation and status."""
    with st.sidebar:
        # Logo and Title
        st.markdown("""
        <div style="text-align: center; margin-bottom: 32px;">
            <div style="display: inline-flex; align-items: center; gap: 8px; margin-bottom: 16px;">
                <span style="font-size: 36px;">🚨</span>
                <div>
                    <h1 style="font-size: 24px; font-weight: 800; background: linear-gradient(135deg, #FF4D4F 0%, #FF8A3D 100%);
                                -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        LifeLine
                    </h1>
                    <p style="font-size: 12px; color: #8B95AD; margin-top: -2px;">
                        Emergency Navigation System
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        render_offline_badge()
        st.divider()

        # Navigation - using real Streamlit buttons
        pages = [
            ("🏠", "Home", "home"),
            ("🗺️", "Emergency Map", "map_page"),
            ("👨‍👩‍👧‍👦", "Family Tracker", "family_page"),
            ("🚨", "Alerts & Sirens", "alerts_page"),
            ("⚙️", "Settings", "settings_page"),
        ]

        current_page = st.session_state.get("current_page", "home")

        for icon, label, key in pages:
            is_active = (key == current_page)
            btn_type = "primary" if is_active else "secondary"

            if st.button(f"{icon}  {label}", key=f"nav_{key}", type=btn_type, use_container_width=True):
                st.session_state.current_page = key
                st.rerun()

        st.divider()

        # System Status Card
        render_section_title("System Status")

        status_col1, status_col2 = st.columns(2)
        with status_col1:
            render_metric_card("Shelters", "15", status="safe")
        with status_col2:
            hazards = st.session_state.get("active_hazard_counts", {})
            total = sum(hazards.values())
            render_metric_card("Hazards", str(total), status="active" if total > 0 else "safe")

        # Hazard Legend
        if hazards:
            st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
            render_section_title("Active Hazards")
            render_hazard_legend(hazards)

        # Last Update
        last_update = st.session_state.get("last_update", datetime.now())
        st.caption(f"Last updated: {last_update.strftime('%H:%M:%S')} | v1.0.0 | Built for Amritsar")

# ──────────────────────────────────────────────
# MAP COMPONENTS
# ──────────────────────────────────────────────
def create_base_map(center: List[float] = None, zoom: int = 13) -> "folium.Map":
    """Create base folium map with custom styling."""
    if not FOLIUM_AVAILABLE:
        raise ImportError("folium not available")
    import folium

    # Use OpenStreetMap tiles (no API key required)
    m = folium.Map(
        location=center or [31.634, 74.8723],
        zoom_start=zoom,
        tiles='OpenStreetMap',
        attr='© OpenStreetMap contributors',
        control_scale=True,
        prefer_canvas=True,
        max_bounds=True,
        min_zoom=10,
        max_zoom=18,
    )

    # Fit to Amritsar bounds
    amritsar_bounds = [[31.55, 74.7], [31.75, 74.95]]
    m.fit_bounds(amritsar_bounds)

    return m

def add_shelter_markers(map_obj, shelters: List[Shelter]):
    """Add shelter markers to the map."""
    if not FOLIUM_AVAILABLE:
        return
    from src.config import SHELTER_ICONS

    for shelter in shelters:
        # Custom shelter icon
        icon_color = "white"
        icon = folium.Icon(
            color=icon_color,
            icon_color=icon_color,
            icon=shelter.icon,
            prefix='glyphicon'
        )

        # Popup content
        popup_html = f"""
        <div style="font-family: Inter, -apple-system, "Segoe UI", Roboto, sans-serif; color: #E8ECF5;">
            <h4 style="margin: 0 0 8px 0;">{shelter.name}</h4>
            <p style="margin: 0 0 8px 0; color: #8B95AD;">
                <strong>Type:</strong> {shelter.type.value}
            </p>
            <p style="margin: 0 0 8px 0; color: #8B95AD;">
                <strong>Capacity:</strong> {shelter.capacity}
            </p>
            <p style="margin: 0; color: #8B95AD;">
                <strong>Distance:</strong> {shelter.distance_km:.1f} km
            </p>
        </div>
        """

        folium.Marker(
            location=[shelter.latitude, shelter.longitude],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=shelter.name,
            icon=icon
        ).add_to(map_obj)

def add_hazard_zones(map_obj, hazards: List[Hazard]):
    """Add hazard zones to the map."""
    for hazard in hazards:
        # Create circle marker
        folium.Circle(
            location=[hazard.latitude, hazard.longitude],
            radius=hazard.radius_m,
            color=hazard.color,
            fill=True,
            fillColor=hazard.color,
            fillOpacity=0.3,
            popup=f"""
            <div style="font-family: Inter, -apple-system, "Segoe UI", Roboto, sans-serif; color: #E8ECF5;">
                <h4 style="margin: 0 0 8px 0;">{hazard.type.value.title()} Hazard</h4>
                <p style="margin: 0; color: #8B95AD;">{hazard.description}</p>
            </div>
            """,
            tooltip=f"{hazard.type.value.title()} Zone - {hazard.severity.value}"
        ).add_to(map_obj)

def add_route_line(map_obj, route_points: List[Dict]):
    """Add animated route line to the map."""
    if not route_points or not FOLIUM_AVAILABLE:
        return

    # Create coordinates list
    coords = [[p['latitude'], p['longitude']] for p in route_points]

    # Add route line with accent color
    folium.PolyLine(
        locations=coords,
        color='#FF8A3D',
        weight=6,
        opacity=0.8,
        popup=f"""
        <div style="font-family: Inter, -apple-system, "Segoe UI", Roboto, sans-serif; color: #E8ECF5;">
            <h4 style="margin: 0;">Safe Route</h4>
            <p style="margin: 0; color: #8B95AD;">Emergency evacuation path</p>
        </div>
        """
    ).add_to(map_obj)

def add_meetup_marker(map_obj, meetup_coords: Coordinates):
    """Add meetup point marker."""
    if not FOLIUM_AVAILABLE:
        return
    folium.Marker(
        location=[meetup_coords.latitude, meetup_coords.longitude],
        popup="Family Meetup Point",
        icon=folium.Icon(color='green', icon='flag', prefix='fa')
    ).add_to(map_obj)

def add_user_location_marker(map_obj, user_coords: Coordinates):
    """Add user location marker."""
    if not FOLIUM_AVAILABLE:
        return
    folium.Marker(
        location=[user_coords.latitude, user_coords.longitude],
        popup="Your Location",
        icon=folium.Icon(color='blue', icon='user', prefix='fa')
    ).add_to(map_obj)

def render_location_input(label: str, key: str):
    """Render styled location input."""
    col1, col2 = st.columns([3, 1])
    with col1:
        lat = st.number_input(
            f"{label} Lat",
            key=f"{key}_lat",
            value=31.634,
            format="%.4f",
            help="Latitude coordinate"
        )
    with col2:
        lon = st.number_input(
            f"{label} Lon",
            key=f"{key}_lon",
            value=74.8723,
            format="%.4f",
            help="Longitude coordinate"
        )
    return {"latitude": lat, "longitude": lon}

# ──────────────────────────────────────────────
# CARD COMPONENTS
# ──────────────────────────────────────────────
def hazard_card(hazard: Hazard) -> str:
    """Generate HTML for hazard card."""
    severity_colors = {
        "low": "#22C55E",
        "medium": "#FCD34D",
        "high": "#F59E0B",
        "critical": "#DC2626"
    }
    severity_color = severity_colors.get(hazard.severity.value, "#8B95AD")

    return f"""
    <div style="
        background: rgba(26, 35, 64, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        border-left: 4px solid {hazard.color};
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
        ">
            <span style="font-size: 28px;">{hazard.icon}</span>
            <div style="flex: 1;">
                <h4 style="
                    margin: 0 0 2px 0;
                    font-size: 18px;
                    font-weight: 700;
                    color: #E8ECF5;
                ">
                    {hazard.type.value.title()} Hazard
                </h4>
                <p style="
                    margin: 0;
                    color: #8B95AD;
                    font-size: 14px;
                "> {hazard.description}</p>
            </div>
            <span style="
                display: inline-flex;
                align-items: center;
                gap: 4px;
                padding: 4px 12px;
                background: {severity_color};
                color: white;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                text-transform: uppercase;
            ">
                {hazard.severity.value.upper()}
            </span>
        </div>
        <div style="
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        ">
            <span style="
                display: inline-flex;
                align-items: center;
                gap: 2px;
                padding: 2px 6px;
                background: #18223D;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                font-size: 10px;
                color: #E8ECF5;
            "> 📍 {hazard.latitude:.3f}, {hazard.longitude:.3f}</span>
            <span style="
                display: inline-flex;
                align-items: center;
                gap: 2px;
                padding: 2px 6px;
                background: #18223D;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                font-size: 10px;
                color: #E8ECF5;
            "> ⭕ {hazard.radius_m}m</span>
            <span style="
                display: inline-flex;
                align-items: center;
                gap: 2px;
                padding: 2px 6px;
                background: #18223D;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                font-size: 10px;
                color: #E8ECF5;
            "> 🕐 {hazard.reported_at.strftime('%H:%M')}</span>
            <span style="
                display: inline-flex;
                align-items: center;
                gap: 2px;
                padding: 2px 6px;
                background: #18223D;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                font-size: 10px;
                color: #E8ECF5;
            "> 📱 {hazard.reported_by}</span>
        </div>
    </div>
    """

def shelter_card(shelter: Shelter) -> str:
    """Generate HTML for shelter card using design system variables."""
    facilities = [f.strip() for f in shelter.facilities.split(',')]
    capacity_pct = (shelter.effective_capacity / shelter.capacity) * 100 if shelter.capacity > 0 else 0

    return f"""
    <div style="
        background: rgba(26, 35, 64, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
    ">
        <div style="
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 12px;
        ">
            <span style="font-size: 32px;">{shelter.icon}</span>
            <div style="flex: 1;">
                <h4 style="
                    margin: 0 0 2px 0;
                    font-size: 18px;
                    font-weight: 700;
                    color: #E8ECF5;
                ">
                    {shelter.name}
                </h4>
                <p style="
                    margin: 0;
                    color: #8B95AD;
                    font-size: 14px;
                ">
                    {shelter.address}
                </p>
            </div>
            <span style="
                display: inline-flex;
                align-items: center;
                gap: 4px;
                padding: 4px 12px;
                background: #3B82F6;
                color: white;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
            ">
                {shelter.distance_km:.1f} km
            </span>
        </div>

        <div style="margin-bottom: 16px;">
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 4px;
            ">
                <span style="
                    font-size: 14px;
                    color: #8B95AD;
                ">Capacity</span>
                <span style="
                    font-size: 14px;
                    font-weight: 600;
                    color: #E8ECF5;
                ">
                    {shelter.effective_capacity} / {shelter.capacity}
                </span>
            </div>
            <div style="
                width: 100%;
                height: 8px;
                background: #18223D;
                border-radius: 4px;
                overflow: hidden;
            ">
                <div style="
                    height: 100%;
                    background: linear-gradient(135deg, #FF4D4F 0%, #FF8A3D 100%);
                    width: {capacity_pct:.1f}%;
                    transition: width 0.3s;
                "></div>
            </div>
        </div>

        <div style="margin-bottom: 16px;">
            <span style="
                font-size: 14px;
                color: #8B95AD;
                margin-right: 8px;
            ">Facilities:</span>
            <div style="
                display: flex;
                gap: 4px;
                flex-wrap: wrap;
            ">
                {"".join([
                    f'<span style="display: inline-flex; align-items: center; gap: 2px; padding: 2px 6px; background: #18223D; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; font-size: 10px; color: #E8ECF5;">{f}</span>' for f in facilities
                ])}
            </div>
        </div>

        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
        ">
            <span style="
                font-size: 14px;
                color: #8B95AD;
            ">
                📞 {shelter.contact_phone}
            </span>
            <span style="
                font-size: 14px;
                color: #8B95AD;
            ">
                👤 {shelter.contact_person}
            </span>
        </div>
    </div>
    """

def family_member_card(member: FamilyMember) -> str:
    """Generate HTML for family member card."""
    status_color = {
        "safe": "#22C55E",
        "unknown": "#F59E0B",
        "needs_help": "#EF4444"
    }.get(member.status, "#8B95AD")

    return f"""
    <div style="
        background: rgba(26, 35, 64, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 12px;
    ">
        <div style="width: 48px; height: 48px; border-radius: 50%; background: #18223D;
                     display: flex; align-items: center; justify-content: center; font-weight: 700;
                     font-size: 20px; color: #E8ECF5;">
            {member.name[0].upper()}
        </div>
        <div style="flex: 1;">
            <h4 style="margin: 0 0 4px 0; font-weight: 600;">{member.name}</h4>
            <p style="margin: 0; color: #8B95AD; font-size: 14px;">
                Last seen: {member.last_seen.strftime('%H:%M:%S')}
            </p>
        </div>
        <div style="display: flex; align-items: center; gap: 4px;">
            <span style="width: 8px; height: 8px; background: {status_color}; border-radius: 50%;"></span>
            <span style="font-size: 14px; color: #8B95AD;">
                {member.status.replace('_', ' ').title()}
            </span>
        </div>
    </div>
    """

# ──────────────────────────────────────────────
# ALERT COMPONENTS
# ──────────────────────────────────────────────
def render_alert_tile(alert_type: str, color: str, title: str):
    """Render alert test tile."""
    if st.button(f"{HAZARD_ICONS.get(alert_type, '🚨')} {title}", type="primary", use_container_width=True, key=f"alert_tile_{alert_type}"):
        st.toast(f"🚨 {title} activated!")

def render_active_alert(alert: Dict):
    """Render active alert item."""
    return f"""
    <div style="
        background: rgba(26, 35, 64, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        border-left: 4px solid {alert['color']};
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0 0 4px 0; font-weight: 600;">{alert['type']}</h4>
                <p style="margin: 0; color: #8B95AD; font-size: 14px;">{alert['description']}</p>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 12px;
        background: {alert['color']};
        color: white;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    ">
                    {alert['severity'].upper()}
                </span>
                <span style="font-size: 12px; color: #8B95AD;">
                    {alert['time']}
                </span>
            </div>
        </div>
    </div>
    """

# ──────────────────────────────────────────────
# EMPTY STATES
# ──────────────────────────────────────────────
def render_empty_hazards():
    """Render empty hazards state."""
    st.markdown(f"""
    <div style="
        background: rgba(26, 35, 64, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 32px;
        margin-bottom: 16px;
        text-align: center;
    ">
        <span style="font-size: 64px;">🌟</span>
        <h3 style="margin: 16px 0; font-weight: 700;">All Clear</h3>
        <p style="color: #8B95AD; margin: 0;">No active hazards detected in your area.</p>
    </div>
    """, unsafe_allow_html=True)

def render_empty_shelters():
    """Render empty shelters state."""
    st.markdown(f"""
    <div style="
        background: rgba(26, 35, 64, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 32px;
        margin-bottom: 16px;
        text-align: center;
    ">
        <span style="font-size: 64px;">🏢</span>
        <h3 style="margin: 16px 0; font-weight: 700;">No Shelters Nearby</h3>
        <p style="color: #8B95AD; margin: 0;">Expand your search radius or try different areas.</p>
    </div>
    """, unsafe_allow_html=True)

def render_empty_family():
    """Render empty family state."""
    st.markdown(f"""
    <div style="
        background: rgba(26, 35, 64, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 32px;
        margin-bottom: 16px;
        text-align: center;
    ">
        <span style="font-size: 64px;">👥</span>
        <h3 style="margin: 16px 0; font-weight: 700;">No Family Group</h3>
        <p style="color: #8B95AD; margin: 0;">Create a group to coordinate with your family during emergencies.</p>
    </div>
    """, unsafe_allow_html=True)

def render_empty_alerts():
    """Render empty alerts state."""
    st.markdown(f"""
    <div style="
        background: rgba(26, 35, 64, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 32px;
        margin-bottom: 16px;
        text-align: center;
    ">
        <span style="font-size: 64px;">✅</span>
        <h3 style="margin: 16px 0; font-weight: 700;">All Clear</h3>
        <p style="color: #8B95AD; margin: 0;">No active alerts. Stay safe!</p>
    </div>
    """, unsafe_allow_html=True)
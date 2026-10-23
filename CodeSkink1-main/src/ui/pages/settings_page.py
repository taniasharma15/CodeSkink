"""
LifeLine Navigator — Settings Page
Offline maps, API keys, hazard weights, app configuration.
"""
import streamlit as st
import textwrap
from src.ui import (
    init_page, init_sidebar, render_emergency_title, render_page_title,
    render_section_title, render_offline_badge
)
from src.api import get_offline_service, get_app_service
from src.config import (
    HAZARD_WEIGHTS, HAZARD_COLORS, HAZARD_ICONS,
    GRID_RESOLUTION_M, MAX_ROUTE_RADIUS_KM, HAZARD_CROSSING_PENALTY,
    OFFLINE_MODE, VIBRATION_PATTERNS, FLASH_COLORS
)


def render_settings_page():
    """Render professional settings page."""
    init_page("LifeLine Navigator — Settings")
    init_sidebar()

    # Header
    header_html = textwrap.dedent("""
        <div style="margin-bottom: var(--spacing-2xl);">
            <h2 style="font-size: 32px; font-weight: 800; margin-bottom: var(--spacing-md);">
                ⚙️ Settings
            </h2>
            <p style="color: var(--text-secondary); font-size: 18px;">
                Configure app preferences, offline maps, and emergency settings
            </p>
        </div>
    """)
    st.markdown(header_html, unsafe_allow_html=True)

    offline_service = get_offline_service()
    app_service = get_app_service()

    # GENERAL SETTINGS
    st.markdown("""
    <div class="glass-card" style="margin-bottom: var(--spacing-2xl);">
        <div style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-xl);">
            <span style="font-size: 36px;">📱</span>
            <div>
                <h3 style="font-size: 24px; font-weight: 700; margin-bottom: var(--spacing-xs);">
                    General Settings
                </h3>
                <p style="color: var(--text-secondary); margin: 0;">
                    Basic app configuration
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📱 App Preferences", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            # Location Services
            st.markdown("""
            <div style="margin-bottom: var(--spacing-md);">
                <label style="display: block; color: var(--text-primary); font-weight: 600; margin-bottom: var(--spacing-sm);">
                    Location Services
                </label>
                <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                            border-radius: var(--radius-md); padding: var(--spacing-md);">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--spacing-sm);">
                        <span>📍 Enable GPS Tracking</span>
                        <div style="width: 44px; height: 24px; background: var(--bg-secondary); border-radius: 12px;
                                    position: relative; cursor: pointer;">
                            <div style="position: absolute; top: 2px; left: 2px; width: 20px; height: 20px;
                                        background: var(--info); border-radius: 50%; transition: all 0.3s;"></div>
                        </div>
                    </div>
                    <div style="color: var(--text-secondary); font-size: 14px;">
                        Share your location with family group
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Notifications
            st.markdown("""
            <div style="margin-bottom: var(--spacing-md);">
                <label style="display: block; color: var(--text-primary); font-weight: 600; margin-bottom: var(--spacing-sm);">
                    Notifications
                </label>
                <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                            border-radius: var(--radius-md); padding: var(--spacing-md);">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--spacing-sm);">
                        <span>🔔 Alert Notifications</span>
                        <div style="width: 44px; height: 24px; background: var(--bg-secondary); border-radius: 12px;
                                    position: relative; cursor: pointer;">
                            <div style="position: absolute; top: 2px; left: 2px; width: 20px; height: 20px;
                                        background: var(--info); border-radius: 50%; transition: all 0.3s;"></div>
                        </div>
                    </div>
                    <div style="color: var(--text-secondary); font-size: 14px;">
                        Receive emergency alerts
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Language
            st.markdown("""
            <div style="margin-bottom: var(--spacing-md);">
                <label style="display: block; color: var(--text-primary); font-weight: 600; margin-bottom: var(--spacing-sm);">
                    Language
                </label>
                <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                            border-radius: var(--radius-md); padding: var(--spacing-md);">
                    <select style="width: 100%; background: transparent; border: none; color: var(--text-primary);
                                  font-size: 15px; padding: 8px;">
                        <option>English (US)</option>
                        <option>Punjabi</option>
                        <option>Hindi</option>
                    </select>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Theme
            st.markdown("""
            <div style="margin-bottom: var(--spacing-md);">
                <label style="display: block; color: var(--text-primary); font-weight: 600; margin-bottom: var(--spacing-sm);">
                    Theme
                </label>
                <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                            border-radius: var(--radius-md); padding: var(--spacing-md);">
                    col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Dark", type="primary", use_container_width=True, key="theme_dark"):
                                st.toast("🌙 Theme set to Dark")
                        with col2:
                            if st.button("Light", type="secondary", use_container_width=True, key="theme_light"):
                                st.toast("☀️ Theme set to Light")
                </div>
            </div>
            """, unsafe_allow_html=True)

    # OFFLINE MAPS
    st.markdown("""
    <div class="glass-card" style="margin-bottom: var(--spacing-2xl);">
        <div style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-xl);">
            <span style="font-size: 36px;">🗺️</span>
            <div>
                <h3 style="font-size: 24px; font-weight: 700; margin-bottom: var(--spacing-xs);">
                    Offline Maps
                </h3>
                <p style="color: var(--text-secondary); margin: 0;">
                    Download maps for use when internet is unavailable
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📴 Offline Map Management", expanded=True):
        # Offline status
        offline_status = offline_service.get_status()

        # Status cards
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 32px; font-weight: 800; margin-bottom: var(--spacing-xs);
                            {'background: var(--success); -webkit-background-clip: text; -webkit-text-fill-color: transparent;' if offline_status.tiles_downloaded else 'color: var(--text-secondary);'}">
                    {'✅' if offline_status.tiles_downloaded else '❌'}
                </div>
                <div style="color: var(--text-secondary); font-size: 14px;">Maps Downloaded</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 32px; font-weight: 800; margin-bottom: var(--spacing-xs);
                            background: var(--info); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {offline_status.size_mb:.1f} MB
                </div>
                <div style="color: var(--text-secondary); font-size: 14px;">Cache Size</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 32px; font-weight: 800; margin-bottom: var(--spacing-xs);
                            background: var(--success); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    Amritsar Metro
                </div>
                <div style="color: var(--text-secondary); font-size: 14px;">Coverage Area</div>
            </div>
            """, unsafe_allow_html=True)

        # Download controls
        st.markdown("""
        <div style="margin-top: var(--spacing-xl);">
            <h4 style="margin-bottom: var(--spacing-md);">Download New Maps</h4>
            <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                        border-radius: var(--radius-md); padding: var(--spacing-md);">
                <div style="margin-bottom: var(--spacing-md);">
                    <label style="display: block; color: var(--text-secondary); font-size: 14px; margin-bottom: var(--spacing-xs);">
                        Select Area to Download
                    </label>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--spacing-md);">
                        <div>
                            <div style="color: var(--text-primary); margin-bottom: var(--spacing-xs);">Min Latitude</div>
                            <input type="number" value="31.55" step="0.001"
                                   style="width: 100%; background: transparent; border: 1px solid var(--border);
                                         border-radius: var(--radius-md); padding: 8px;">
                        </div>
                        <div>
                            <div style="color: var(--text-primary); margin-bottom: var(--spacing-xs);">Max Latitude</div>
                            <input type="number" value="31.75" step="0.001"
                                   style="width: 100%; background: transparent; border: 1px solid var(--border);
                                         border-radius: var(--radius-md); padding: 8px;">
                        </div>
                        <div>
                            <div style="color: var(--text-primary); margin-bottom: var(--spacing-xs);">Min Longitude</div>
                            <input type="number" value="74.7" step="0.001"
                                   style="width: 100%; background: transparent; border: 1px solid var(--border);
                                         border-radius: var(--radius-md); padding: 8px;">
                        </div>
                        <div>
                            <div style="color: var(--text-primary); margin-bottom: var(--spacing-xs);">Max Longitude</div>
                            <input type="number" value="74.95" step="0.001"
                                   style="width: 100%; background: transparent; border: 1px solid var(--border);
                                         border-radius: var(--radius-md); padding: 8px;">
                        </div>
                    </div>
                </div>
                col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📥 Download Maps", type="primary", use_container_width=True, key="download_maps"):
                            st.toast("📥 Starting map download...")
                    with col2:
                        if st.button("🗑️ Clear Cache", type="secondary", use_container_width=True, key="clear_cache"):
                            st.toast("🗑️ Cache cleared")
            </div>
        </div>
        """, unsafe_allow_html=True)

    # HAZARD SETTINGS
    st.markdown("""
    <div class="glass-card" style="margin-bottom: var(--spacing-2xl);">
        <div style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-xl);">
            <span style="font-size: 36px;">⚠️</span>
            <div>
                <h3 style="font-size: 24px; font-weight: 700; margin-bottom: var(--spacing-xs);">
                    Hazard Configuration
                </h3>
                <p style="color: var(--text-secondary); margin: 0;">
                    Customize hazard detection and routing preferences
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("⚙️ Hazard Weights", expanded=True):
        st.markdown("""
        <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                    border-radius: var(--radius-md); padding: var(--spacing-md); margin-bottom: var(--spacing-md);">
            <p style="color: var(--text-secondary); margin-bottom: var(--spacing-md);">
                Adjust how much the routing algorithm avoids different hazard types.
                Higher values = stronger avoidance.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Hazard weight sliders
        for hazard_type, weight in HAZARD_WEIGHTS.items():
            col_label, col_slider = st.columns([2, 3])
            with col_label:
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: var(--spacing-sm);">
                    <span style="font-size: 24px;">{HAZARD_ICONS[hazard_type]}</span>
                    <span style="font-weight: 600;">{hazard_type.title()}</span>
                </div>
                """, unsafe_allow_html=True)
            with col_slider:
                new_weight = st.slider(
                    f"Weight for {hazard_type}",
                    min_value=0.0,
                    max_value=20.0,
                    value=weight,
                    step=0.5,
                    format="%.1f"
                )

    # ALERTS SETTINGS
    st.markdown("""
    <div class="glass-card" style="margin-bottom: var(--spacing-2xl);">
        <div style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-xl);">
            <span style="font-size: 36px;">🔔</span>
            <div>
                <h3 style="font-size: 24px; font-weight: 700; margin-bottom: var(--spacing-xs);">
                    Alert Settings
                </h3>
                <p style="color: var(--text-secondary); margin: 0;">
                    Configure alert preferences and notification channels
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔔 Alert Preferences", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            # Alert types
            st.markdown("""
            <div style="margin-bottom: var(--spacing-md);">
                <label style="display: block; color: var(--text-primary); font-weight: 600; margin-bottom: var(--spacing-sm);">
                    Enable Alert Types
                </label>
                <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                            border-radius: var(--radius-md); padding: var(--spacing-md);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--spacing-sm);">
                        <span style="display: flex; align-items: center; gap: var(--spacing-sm);">
                            <span style="font-size: 20px;">🌊</span> Flood Alerts
                        </span>
                        <div style="width: 44px; height: 24px; background: var(--info); border-radius: 12px;
                                    position: relative; cursor: pointer;">
                            <div style="position: absolute; top: 2px; right: 2px; width: 20px; height: 20px;
                                        background: white; border-radius: 50%; transition: all 0.3s;"></div>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--spacing-sm);">
                        <span style="display: flex; align-items: center; gap: var(--spacing-sm);">
                            <span style="font-size: 20px;">🔥</span> Fire Alerts
                        </span>
                        <div style="width: 44px; height: 24px; background: var(--info); border-radius: 12px;
                                    position: relative; cursor: pointer;">
                            <div style="position: absolute; top: 2px; right: 2px; width: 20px; height: 20px;
                                        background: white; border-radius: 50%; transition: all 0.3s;"></div>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="display: flex; align-items: center; gap: var(--spacing-sm);">
                            <span style="font-size: 20px;">👥</span> Family Alerts
                        </span>
                        <div style="width: 44px; height: 24px; background: var(--info); border-radius: 12px;
                                    position: relative; cursor: pointer;">
                            <div style="position: absolute; top: 2px; right: 2px; width: 20px; height: 20px;
                                        background: white; border-radius: 50%; transition: all 0.3s;"></div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Sensitivity
            sensitivity = st.slider(
                "Alert Sensitivity",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                format="%.1f"
            )
            st.markdown("""
            <div style="color: var(--text-secondary); font-size: 14px; margin-top: var(--spacing-xs);">
                Higher sensitivity = more alerts, may increase false positives
            </div>
            """, unsafe_allow_html=True)

    # API SETTINGS
    st.markdown("""
    <div class="glass-card" style="margin-bottom: var(--spacing-2xl);">
        <div style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-xl);">
            <span style="font-size: 36px;">🔌</span>
            <div>
                <h3 style="font-size: 24px; font-weight: 700; margin-bottom: var(--spacing-xs);">
                    API Configuration
                </h3>
                <p style="color: var(--text-secondary); margin: 0;">
                    External service integrations (optional)
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🌐 External Services", expanded=True):
        # OpenWeather API
        st.markdown("""
        <div style="margin-bottom: var(--spacing-xl);">
            <h4 style="margin-bottom: var(--spacing-md);">Weather API (OpenWeatherMap)</h4>
            <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                        border-radius: var(--radius-md); padding: var(--spacing-md);">
                <div style="margin-bottom: var(--spacing-md);">
                    <label style="display: block; color: var(--text-secondary); font-size: 14px; margin-bottom: var(--spacing-xs);">
                        API Key
                    </label>
                    <input type="password" placeholder="Enter your API key"
                           style="width: 100%; background: transparent; border: 1px solid var(--border);
                                 border-radius: var(--radius-md); padding: 10px;">
                </div>
                if st.button("🔑 Save API Key", type="secondary", use_container_width=True, key="save_api_key"):
                    st.toast("🔑 API key saved")
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Routing Service
        st.markdown("""
        <div>
            <h4 style="margin-bottom: var(--spacing-md);">Routing Service (OpenRouteService)</h4>
            <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                        border-radius: var(--radius-md); padding: var(--spacing-md);">
                <div style="margin-bottom: var(--spacing-md);">
                    <label style="display: block; color: var(--text-secondary); font-size: 14px; margin-bottom: var(--spacing-xs);">
                        API Key
                    </label>
                    <input type="password" placeholder="Enter your API key (optional)"
                           style="width: 100%; background: transparent; border: 1px solid var(--border);
                                 border-radius: var(--radius-md); padding: 10px;">
                </div>
                if st.button("🔑 Save API Key", type="secondary", use_container_width=True, key="save_api_key"):
                    st.toast("🔑 API key saved")
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: var(--spacing-2xl); padding: var(--spacing-xl);
                 border-top: 1px solid var(--border); color: var(--text-secondary);">
        <p style="margin: 0; font-size: var(--font-size-sm);">
            All settings saved locally • Privacy-first • Offline capable
        </p>
        <p style="margin: var(--spacing-xs) 0 0 0; font-size: var(--font-size-xs);">
            Version 1.0 • Built for Amritsar Emergency Network
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_settings_page()
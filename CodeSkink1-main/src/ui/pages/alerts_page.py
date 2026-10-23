"""
LifeLine Navigator — Alerts & Accessibility Page
Siren detection, vibration patterns, visual flashes for deaf/HoH users.
"""
import streamlit as st
import textwrap
import time
from src.ui import (
    init_page, init_sidebar, render_emergency_title, render_page_title,
    render_section_title, render_offline_badge
)
from src.api import get_alert_manager
from src.config import VIBRATION_PATTERNS, FLASH_COLORS, HAZARD_ICONS


def render_alerts_page():
    """Render professional alerts & accessibility page."""
    init_page("LifeLine Navigator — Alerts & Accessibility")
    init_sidebar()

    # Header
    header_html = textwrap.dedent("""
        <div style="margin-bottom: var(--spacing-2xl);">
            <h2 style="font-size: 32px; font-weight: 800; margin-bottom: var(--spacing-md);">
                🚨 Alerts & Accessibility
            </h2>
            <p style="color: var(--text-secondary); font-size: 18px;">
                Multi-sensory alerts for emergency situations
            </p>
        </div>
    """)
    st.markdown(header_html, unsafe_allow_html=True)

    # Emergency contacts
    st.markdown("""
    <div style="margin-bottom: var(--spacing-xl); display: flex; gap: var(--spacing-sm); flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: var(--spacing-xs); padding: 6px 16px;
                     background: rgba(239, 68, 68, 0.2); border: 1px solid #EF4444;
                     border-radius: 20px; font-size: 14px; font-weight: 600;">
            <span>🚨 Emergency Hotline: 112</span>
            <span>🆘 SOS: 108</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    alert_manager = get_alert_manager()

    # SIREN DETECTION SECTION
    st.markdown("""
    <div class="glass-card" style="margin-bottom: var(--spacing-2xl);">
        <div style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-xl);">
            <span style="font-size: 36px;">🎤</span>
            <div>
                <h3 style="font-size: 24px; font-weight: 700; margin-bottom: var(--spacing-xs);">
                    Smart Siren Detection
                </h3>
                <p style="color: var(--text-secondary); margin: 0;">
                    Real-time audio analysis for emergency sounds
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        # Detection info
        st.markdown("""
        <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                    border-radius: var(--radius-lg); padding: var(--spacing-md); margin-bottom: var(--spacing-md);">
            <h4 style="font-size: 18px; font-weight: 600; margin-bottom: var(--spacing-md);">
                🔬 How It Works
            </h4>
            <ul style="color: var(--text-secondary); line-height: 1.8;">
                <li>🎙️ Microphone listens for emergency sirens</li>
                <li>🧠 AI analyzes audio patterns locally</li>
                <li>⚡ Triggers alerts within 2-3 seconds</li>
                <li>🔒 All processing stays on your device</li>
            </ul>
        </div>

        <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                    border-radius: var(--radius-lg); padding: var(--spacing-md); margin-bottom: var(--spacing-md);">
            <h4 style="font-size: 18px; font-weight: 600; margin-bottom: var(--spacing-md);">
                🎯 Detection Types
            </h4>
            <div style="display: grid; gap: var(--spacing-md);">
                <div style="display: flex; align-items: center; gap: var(--spacing-sm);">
                    <span style="font-size: 24px;">🌊</span>
                    <div>
                        <div style="font-weight: 600;">Flood/Cyclone</div>
                        <div style="color: var(--text-secondary); font-size: 14px;">Low frequency sweep</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: var(--spacing-sm);">
                    <span style="font-size: 24px;">🔥</span>
                    <div>
                        <div style="font-weight: 600;">Fire/Ambulance</div>
                        <div style="color: var(--text-secondary); font-size: 14px;">Fast frequency sweep</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: var(--spacing-sm);">
                    <span style="font-size: 24px;">🏃</span>
                    <div>
                        <div style="font-weight: 600;">Evacuation</div>
                        <div style="color: var(--text-secondary); font-size: 14px;">Modulated wail</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Sensitivity slider
        sensitivity = st.slider(
            "Detection Sensitivity",
            min_value=0.0,
            max_value=1.0,
            value=0.68,
            step=0.01,
            format="%.2f"
        )
        st.markdown(f"""
        <div style="color: var(--text-secondary); font-size: 14px; margin-top: var(--spacing-xs);">
            Higher values detect more sounds but may have false positives
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Listening control
        listening = st.session_state.get("siren_listening", False)

        if not listening:
            if st.button("🎤 Start Listening", type="primary", use_container_width=False, key="start_listening"):
                st.session_state.siren_listening = True
                st.toast("🎤 Started listening for sirens...")
                st.rerun()
        else:
            # Active listening
            active_html = textwrap.dedent("""
                <div style="text-align: center;">
                    <div style="width: 200px; height: 200px; border-radius: 50%;
                                background: var(--accent-gradient); display: flex;
                                flex-direction: column; align-items: center; justify-content: center;
                                gap: var(--spacing-md); position: relative; margin: 0 auto;">
                        <div style="position: absolute; inset: 0; border-radius: 50%;
                                    border: 3px solid rgba(255, 138, 61, 0.5);
                                    animation: pulse-ring 2s infinite;"></div>
                        <span style="font-size: 48px; z-index: 1;">🎤</span>
                        <span style="font-weight: 700; z-index: 1;">Listening...</span>
                    </div>
                    if st.button("⏹️ Stop Listening", type="secondary", use_container_width=False, key="stop_listening"):
                st.session_state.siren_listening = False
                st.toast("🛑 Stopped listening")
                st.rerun()
                </div>
            """)
            st.markdown(active_html, unsafe_allow_html=True)

        # Detection stats
        st.markdown("""
        <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                    border-radius: var(--radius-lg); padding: var(--spacing-md); margin-top: var(--spacing-md);">
            <h4 style="font-size: 18px; font-weight: 600; margin-bottom: var(--spacing-md); text-align: center;">
                Detection Stats
            </h4>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--spacing-md); text-align: center;">
                <div>
                    <div style="font-size: 24px; font-weight: 800;">0</div>
                    <div style="color: var(--text-secondary); font-size: 12px;">Frames</div>
                </div>
                <div>
                    <div style="font-size: 24px; font-weight: 800;">0</div>
                    <div style="color: var(--text-secondary); font-size: 12px;">Detections</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ALERT TEST BUTTONS
    st.markdown("""
    <div class="glass-card" style="margin-bottom: var(--spacing-2xl);">
        <div style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-xl);">
            <span style="font-size: 36px;">🔔</span>
            <div>
                <h3 style="font-size: 24px; font-weight: 700; margin-bottom: var(--spacing-xs);">
                    Test Emergency Alerts
                </h3>
                <p style="color: var(--text-secondary); margin: 0;">
                    Experience different alert types and patterns
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Alert test tiles grid
    alert_types = [
        ("Flood Alert", "🌊", FLASH_COLORS["flood"], "flood"),
        ("Fire Alert", "🔥", FLASH_COLORS["fire"], "fire"),
        ("Evacuate", "🏃", FLASH_COLORS["evacuate"], "evacuate"),
        ("All Clear", "✅", FLASH_COLORS["all_clear"], "all_clear")
    ]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        alert_name, icon, color, alert_type = alert_types[0]
        if st.button(f"{icon} {alert_name}", type="primary", use_container_width=True, key=f"alert_{alert_type}"):
            st.toast(f"🚨 {alert_name} activated!")

    with col2:
        alert_name, icon, color, alert_type = alert_types[1]
        if st.button(f"{icon} {alert_name}", type="primary", use_container_width=True, key=f"alert_{alert_type}"):
            st.toast(f"🚨 {alert_name} activated!")

    with col3:
        alert_name, icon, color, alert_type = alert_types[2]
        if st.button(f"{icon} {alert_name}", type="primary", use_container_width=True, key=f"alert_{alert_type}"):
            st.toast(f"🚨 {alert_name} activated!")

    with col4:
        alert_name, icon, color, alert_type = alert_types[3]
        if st.button(f"{icon} {alert_name}", type="primary", use_container_width=True, key=f"alert_{alert_type}"):
            st.toast(f"🚨 {alert_name} activated!")

    # VIBRATION PATTERNS
    st.markdown("""
    <div class="glass-card" style="margin-bottom: var(--spacing-2xl);">
        <div style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-xl);">
            <span style="font-size: 36px;">📳</span>
            <div>
                <h3 style="font-size: 24px; font-weight: 700; margin-bottom: var(--spacing-xs);">
                    Vibration Patterns
                </h3>
                <p style="color: var(--text-secondary); margin: 0;">
                    Unique patterns for different alert types
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Pattern display
    pattern_container = textwrap.dedent("""
        <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                    border-radius: var(--radius-lg); padding: var(--spacing-md); margin-bottom: var(--spacing-md);">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--spacing-md);">
                <h4 style="font-size: 18px; font-weight: 600;">Pattern Preview</h4>
                if st.button("▶️ Test Vibration", type="secondary", key="test_vibration"):
                    st.toast("📳 Testing vibration pattern...")
            </div>
            <div style="display: flex; align-items: center; gap: var(--spacing-sm);">
                <span style="font-size: 24px;">🌊</span>
                <div style="flex: 1;">
                    <div style="display: flex; gap: 4px; align-items: center;">
                        <div style="width: 20px; height: 20px; border-radius: 4px; background: #FF8A3D;"></div>
                        <div style="width: 20px; height: 20px; border-radius: 4px; background: transparent; border: 1px solid var(--border);"></div>
                        <div style="width: 20px; height: 20px; border-radius: 4px; background: #FF8A3D;"></div>
                        <div style="width: 20px; height: 20px; border-radius: 4px; background: transparent; border: 1px solid var(--border);"></div>
                        <div style="width: 20px; height: 20px; border-radius: 4px; background: #FF8A3D;"></div>
                    </div>
                    <div style="color: var(--text-secondary); font-size: 12px; margin-top: 4px;">
                        500ms - 200ms - 500ms - 200ms - 500ms
                    </div>
                </div>
            </div>
        </div>
    """)
    st.markdown(pattern_container, unsafe_allow_html=True)

    # Manual Broadcast Section
    st.markdown("""
    <div class="glass-card" style="margin-bottom: var(--spacing-2xl);">
        <div style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-xl);">
            <span style="font-size: 36px;">📢</span>
            <div>
                <h3 style="font-size: 24px; font-weight: 700; margin-bottom: var(--spacing-xs);">
                    Manual Alert Broadcast
                </h3>
                <p style="color: var(--text-secondary); margin: 0;">
                    Send custom alerts to your family group
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Broadcast form
    with st.form("broadcast_form"):
        alert_type = st.selectbox(
            "Alert Type",
            ["Information", "Warning", "Danger", "Safe"]
        )
        message = st.text_area(
            "Message",
            placeholder="Enter your alert message...",
            height=100
        )

        col1, col2 = st.columns(2)
        with col1:
            include_vibration = st.checkbox("Include Vibration", value=True)
        with col2:
            include_flash = st.checkbox("Include Flash", value=True)

        submitted = st.form_submit_button("📤 Send Alert", type="primary", use_container_width=True)

        if submitted:
            st.success("✅ Alert sent to family group!")

    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: var(--spacing-2xl); padding: var(--spacing-xl);
                 border-top: 1px solid var(--border); color: var(--text-secondary);">
        <p style="margin: 0; font-size: var(--font-size-sm);">
            Multi-sensory alerts • Accessibility first • Offline capable
        </p>
    </div>
    """, unsafe_allow_html=True)


# Visual Flash Preview (for demonstration)
def flash_preview():
    """Create a visual flash effect for demo purposes."""
    st.markdown("""
    <div id="flash-preview" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                                   background: #FF4D4F; opacity: 0; pointer-events: none;
                                   transition: opacity 0.3s ease; z-index: 9999;">
    </div>
    <script>
        // Flash animation
        setTimeout(() => {
            document.getElementById('flash-preview').style.opacity = '0.3';
            setTimeout(() => {
                document.getElementById('flash-preview').style.opacity = '0';
            }, 300);
        }, 100);
    </script>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_alerts_page()
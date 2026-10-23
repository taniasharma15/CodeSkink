"""
LifeLine Navigator — Design System & Global Styles
Professional emergency navigation UI with dark command center theme.
"""
import textwrap
from typing import List, Dict, Optional
import streamlit as st

# ──────────────────────────────────────────────
# CSS VARIABLES & DESIGN TOKENS
# ──────────────────────────────────────────────

CSS_VARIABLES = """
:root {
    /* Theme Colors - Modern Dark Command Center */
    --bg-primary: #0B1020;
    --bg-secondary: #121A2F;
    --bg-tertiary: #18223D;
    --bg-card: rgba(26, 35, 64, 0.6);
    --border: rgba(255, 255, 255, 0.08);
    --text-primary: #E8ECF5;
    --text-secondary: #8B95AD;
    --text-muted: #6B7280;

    /* Emergency Colors */
    --accent-gradient: linear-gradient(135deg, #FF4D4F 0%, #FF8A3D 100%);
    --success: #22C55E;
    --warning: #F59E0B;
    --info: #3B82F6;
    --danger: #EF4444;

    /* Severity Colors */
    --severity-critical: #DC2626;
    --severity-high: #F59E0B;
    --severity-medium: #FCD34D;
    --severity-low: #22C55E;

    /* Typography */
    --font-family: "Inter", -apple-system, "Segoe UI", Roboto, sans-serif;
    --font-size-xs: 12.5px;
    --font-size-sm: 14px;
    --font-size-base: 15px;
    --font-size-lg: 18px;
    --font-size-xl: 20px;
    --font-size-2xl: 24px;
    --font-size-3xl: 32px;
    --font-size-4xl: 40px;

    /* Spacing */
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;
    --spacing-2xl: 48px;

    /* Border Radius */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 24px;

    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.1);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    --shadow-glow: 0 0 20px rgba(255, 77, 79, 0.3);

    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-base: 300ms ease;
    --transition-slow: 500ms ease;
}

/* Reset & Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--font-family);
    background: var(--bg-primary);
    background-image:
        radial-gradient(circle at 20% 80%, rgba(255, 77, 79, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.1) 0%, transparent 50%);
    color: var(--text-primary);
    font-size: var(--font-size-base);
    line-height: 1.6;
    min-height: 100vh;
}

/* Hide Streamlit elements */
.css-1d391kg { /* Streamlit main menu */
    visibility: hidden !important;
}
.css-1vq3dl6 { /* Streamlit footer */
    visibility: hidden !important;
}
footer { /* Generic footer */
    display: none !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
    background: var(--text-secondary);
    border-radius: var(--radius-sm);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-primary);
}

/* Text Selection */
::selection {
    background: var(--accent-gradient);
    color: white;
}

/* Custom Animations */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

@keyframes pulse-ring {
    0% {
        transform: scale(1);
        opacity: 1;
    }
    100% {
        transform: scale(1.5);
        opacity: 0;
    }
}

@keyframes count-up {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

@keyframes slide-in {
    from { transform: translateX(100%); }
    to { transform: translateX(0); }
}

@keyframes glow-pulse {
    0%, 100% { box-shadow: 0 0 20px rgba(255, 77, 79, 0.4); }
    50% { box-shadow: 0 0 30px rgba(255, 77, 79, 0.8); }
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* Utility Classes */
.gradient-text {
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.glass-card {
    background: var(--bg-card);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: var(--spacing-md);
    transition: transform var(--transition-base), box-shadow var(--transition-base);
    animation: count-up var(--transition-base) ease-out;
}

.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg), var(--shadow-glow);
}

.severity-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: var(--font-size-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.severity-critical {
    background: var(--severity-critical);
    color: white;
}

.severity-high {
    background: var(--severity-high);
    color: white;
}

.severity-medium {
    background: var(--severity-medium);
    color: #1F2937;
}

.severity-low {
    background: var(--severity-low);
    color: white;
}

/* Custom Buttons */
.btn-primary {
    background: var(--accent-gradient);
    color: white;
    border: none;
    border-radius: var(--radius-md);
    padding: 12px 24px;
    font-size: var(--font-size-base);
    font-weight: 600;
    height: 44px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: all var(--transition-base);
    position: relative;
    overflow: hidden;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(255, 77, 79, 0.3);
}

.btn-primary:active {
    transform: translateY(0);
    box-shadow: 0 4px 8px rgba(255, 77, 79, 0.2);
}

.btn-secondary {
    background: transparent;
    color: var(--text-primary);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 11px 23px;
    font-size: var(--font-size-base);
    font-weight: 500;
    height: 44px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: all var(--transition-base);
}

.btn-secondary:hover {
    background: var(--bg-tertiary);
    border-color: var(--text-secondary);
}

/* Custom Streamlit Widgets */
.stButton > button {
    border-radius: var(--radius-md);
    height: 44px;
    font-weight: 600;
    transition: all var(--transition-base);
}

.stButton > button:hover {
    transform: translateY(-2px);
}

.stTabs [data-baseweb="tab-list"] {
    gap: var(--spacing-xs);
    background: transparent;
    padding: var(--spacing-xs);
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
}

.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm);
    padding: 8px 20px;
    font-weight: 600;
    transition: all var(--transition-base);
}

.stTabs [data-baseweb="tab"][data-state="active"] {
    background: var(--bg-tertiary);
    border-bottom: 2px solid var(--text-primary);
}

.stNumberInput input, .stTextInput input, .stSelectbox select {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    padding: 10px 14px !important;
    transition: all var(--transition-base);
}

.stNumberInput input:focus, .stTextInput input:focus, .stSelectbox select:focus {
    outline: 2px solid var(--info) !important;
    outline-offset: 2px;
}

/* Toast Messages */
.success-toast {
    background: var(--success);
    color: white;
    padding: 16px 24px;
    border-radius: var(--radius-md);
    margin-bottom: var(--spacing-md);
    animation: slide-in var(--transition-base) ease-out;
}

.error-toast {
    background: var(--danger);
    color: white;
    padding: 16px 24px;
    border-radius: var(--radius-md);
    margin-bottom: var(--spacing-md);
    animation: slide-in var(--transition-base) ease-out;
}

/* Map Styles */
.map-container {
    width: 100%;
    height: 600px;
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}

.folium-map {
    background: #1a1a1a !important;
}

/* Loading Spinner */
.custom-spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: var(--text-primary);
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Live Status Pill */
.live-status {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: 6px 16px;
    background: rgba(34, 197, 94, 0.2);
    border: 1px solid var(--success);
    border-radius: 20px;
    color: var(--success);
    font-size: var(--font-size-sm);
    font-weight: 600;
    pointer-events: none !important;
}

.live-dot {
    width: 8px;
    height: 8px;
    background: var(--success);
    border-radius: 50%;
    animation: pulse 2s infinite;
}

/* Hazard Legend */
.hazard-legend {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
}

.hazard-legend-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
}

.hazard-legend-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

/* Progress Bars */
.progress-bar {
    width: 100%;
    height: 8px;
    background: var(--bg-tertiary);
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: var(--accent-gradient);
    transition: width var(--transition-base);
}

/* Contact Chips */
.contact-chip {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: 6px 14px;
    background: var(--bg-tertiary);
    border: 1px solid var(--border);
    border-radius: 20px;
    color: var(--text-primary);
    font-size: var(--font-size-sm);
    transition: all var(--transition-base);
}

.contact-chip:hover {
    background: var(--bg-secondary);
    border-color: var(--text-secondary);
}

/* Responsive */
@media (max-width: 768px) {
    .glass-card {
        margin-bottom: var(--spacing-md);
    }

    .kpi-grid {
        grid-template-columns: 1fr !important;
    }

    .two-column {
        flex-direction: column !important;
    }
}
"""

# ──────────────────────────────────────────────
# HTML HELPERS
# ──────────────────────────────────────────────

def dedent_html(html: str) -> str:
    """Remove leading whitespace from HTML to prevent code block rendering."""
    return textwrap.dedent(html).strip()

def build_hazard_legend_item(hazard_type: str, color: str, count: int) -> str:
    """Build a single hazard legend item without indentation."""
    return f"""
    <div class="hazard-legend-item">
        <span class="hazard-legend-dot" style="background: {color}"></span>
        <span class="hazard-legend-text">{hazard_type.title()}: {count}</span>
    </div>
    """

# ──────────────────────────────────────────────
# STYLES & CONFIGURATION
# ──────────────────────────────────────────────

def inject_main_css():
    """Inject the complete design system CSS."""
    st.markdown(f"""
    <style>
    {CSS_VARIABLES}
    </style>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# COMPONENT STYLING FUNCTIONS
# ──────────────────────────────────────────────

def render_emergency_title(icon: str, title: str):
    """Render styled emergency title."""
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-xl);">
        <span style="font-size: var(--font-size-4xl);">{icon}</span>
        <div>
            <h1 style="font-size: var(--font-size-3xl); font-weight: 800; margin-bottom: var(--spacing-xs);">{title}</h1>
            <p style="color: var(--text-secondary); font-size: var(--font-size-lg);">Navigate safely when every second counts</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_page_title(title: str, subtitle: str = ""):
    """Render page title with subtitle."""
    st.markdown(f"""
    <div style="margin-bottom: var(--spacing-2xl);">
        <h2 style="font-size: var(--font-size-3xl); font-weight: 800; margin-bottom: var(--spacing-md);">
            {title}
        </h2>
        {f'<p style="color: var(--text-secondary); font-size: var(--font-size-xl);">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def render_section_title(title: str):
    """Render section title with divider."""
    st.markdown(f"""
    <div style="margin-bottom: var(--spacing-lg);">
        <h3 style="font-size: var(--font-size-xl); font-weight: 700; margin-bottom: var(--spacing-sm); display: flex; align-items: center; gap: var(--spacing-sm);">
            {title}
            <div style="flex: 1; height: 1px; background: var(--border);"></div>
        </h3>
    </div>
    """, unsafe_allow_html=True)

def render_status_badge(status: str, is_online: bool = True):
    """Render status badge."""
    if status == "safe":
        color = var('--success')
        text = "Safe"
    elif status == "active":
        color = var('--warning')
        text = "Active"
    elif status == "warning":
        color = var('--warning')
        text = "Warning"
    else:
        color = var('--text-secondary')
        text = status

    status_html = f"""
    <span style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px; background: {color}20;
                 border: 1px solid {color}; border-radius: 20px; font-size: var(--font-size-sm); font-weight: 600;">
        {text}
    </span>
    """
    st.markdown(status_html, unsafe_allow_html=True)

def render_metric_card(label: str, value: str, status: str = "safe"):
    """Render metric card with status indicator."""
    status_color = {
        "safe": var('--success'),
        "active": var('--warning'),
        "warning": var('--warning'),
        "offline": var('--text-secondary')
    }.get(status, var('--text-secondary'))

    metric_html = f"""
    <div class="glass-card" style="text-align: center; animation-delay: 0.1s;">
        <div style="font-size: var(--font-size-4xl); font-weight: 800; margin-bottom: var(--spacing-xs);
                    background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            {value}
        </div>
        <div style="color: var(--text-secondary); font-size: var(--font-size-sm); font-weight: 500;">
            {label}
        </div>
        <div style="margin-top: var(--spacing-xs);">
            <span style="display: inline-block; width: 8px; height: 8px; background: {status_color};
                         border-radius: 50%; animation: pulse 2s infinite;"></span>
        </div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)

def render_hazard_legend(hazards: Dict[str, int]):
    """Render hazard legend without raw HTML."""
    legend_items = []
    hazard_colors = {
        'flood': '#1E90FF',
        'fire': '#FF4444',
        'debris': '#8B4513',
        'crowd': '#FFA500',
        'traffic': '#FFFF00',
        'landslide': '#808080',
        'chemical': '#800080',
        'structural': '#FF00FF'
    }

    for hazard_type, count in hazards.items():
        color = hazard_colors.get(hazard_type, '#888888')
        legend_items.append(build_hazard_legend_item(hazard_type.title(), color, count))

    legend_html = f"""
    <div class="hazard-legend">
        {''.join(legend_items)}
    </div>
    """
    st.markdown(legend_html, unsafe_allow_html=True)

def render_offline_badge():
    """Render offline mode badge."""
    badge_html = f"""
    <span style="display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px;
                 background: rgba(34, 197, 94, 0.2); border: 1px solid var(--success);
                 border-radius: 16px; font-size: var(--font-size-xs); font-weight: 600;">
        📶 Offline Mode
    </span>
    """
    st.markdown(badge_html, unsafe_allow_html=True)

def render_emergency_contacts():
    """Render emergency contact chips."""
    contacts = [
        ("112", "National Emergency"),
        ("101", "Fire"),
        ("102/108", "Ambulance"),
        ("100", "Police")
    ]

    contacts_html = f"""
    <div style="display: flex; gap: var(--spacing-sm); flex-wrap: wrap;">
        {"".join([f'<div class="contact-chip"><strong>{num}</strong> {name}</div>' for num, name in contacts])}
    </div>
    """
    st.markdown(contacts_html, unsafe_allow_html=True)

def render_live_status():
    """Render LIVE status pill."""
    status_html = f"""
    <div class="live-status" style="position: fixed; top: 20px; right: 20px; z-index: 999; background: rgba(34, 197, 94, 0.1); backdrop-filter: blur(10px); pointer-events: none;">
        <span class="live-dot"></span>
        <span>LIVE</span>
    </div>
    """
    st.markdown(status_html, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# COLOR HELPERS
# ──────────────────────────────────────────────

def var(name: str) -> str:
    """Get CSS variable value."""
    return f"var(--{name})"

def get_severity_color(severity: str) -> str:
    """Get color for severity level."""
    severity_colors = {
        'critical': 'var(--severity-critical)',
        'high': 'var(--severity-high)',
        'medium': 'var(--severity-medium)',
        'low': 'var(--severity-low)'
    }
    return severity_colors.get(severity.lower(), 'var(--text-secondary)')

# ──────────────────────────────────────────────
# ANIMATION HELPERS
# ──────────────────────────────────────────────

def animate_element(element_id: str, animation: str = "count-up", duration: str = "300ms"):
    """Add CSS animation to element."""
    st.markdown(f"""
    <style>
    #{element_id} {{
        animation: {animation} {duration} ease-out;
    }}
    </style>
    """, unsafe_allow_html=True)
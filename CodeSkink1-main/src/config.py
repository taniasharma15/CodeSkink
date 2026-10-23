"""
LifeLine Navigator — Configuration for Amritsar
Centralized constants, city bounds, hazard weights, and settings.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────
# CITY CONFIGURATION — AMRITSAR
# ──────────────────────────────────────────────
CITY_NAME = "Amritsar"
CITY_STATE = "Punjab"
CITY_COUNTRY = "India"

# Map bounds [min_lat, min_lon, max_lat, max_lon] — covers Amritsar metro
AMRITSAR_BOUNDS = {
    "min_lat": 31.55,
    "min_lon": 74.70,
    "max_lat": 31.75,
    "max_lon": 74.95,
}

# Map center for initial view
MAP_CENTER = [31.6340, 74.8723]  # Golden Temple area
MAP_ZOOM_START = 12
MAP_ZOOM_MIN = 10
MAP_ZOOM_MAX = 18

# ──────────────────────────────────────────────
# HAZARD WEIGHTS — Tune these manually for demo
# Higher = avoid more aggressively
# ──────────────────────────────────────────────
HAZARD_WEIGHTS = {
    "flood": 10.0,       # Deep water — impassable
    "fire": 8.0,         # Active fire perimeter
    "debris": 5.0,       # Building collapse, fallen trees
    "crowd": 3.0,        # Protest, stampede risk
    "traffic": 2.0,      # Congestion (normal routing handles this)
    "landslide": 9.0,    # Mountain areas (less relevant for Amritsar)
    "chemical": 10.0,    # Industrial hazard
    "structural": 7.0,   # Damaged buildings
}

# Hazard display colors (for map legend)
HAZARD_COLORS = {
    "flood": "#1e90ff",      # Blue
    "fire": "#ff4444",       # Red
    "debris": "#8b4513",     # Brown
    "crowd": "#ffa500",      # Orange
    "traffic": "#ffff00",    # Yellow
    "landslide": "#808080",  # Gray
    "chemical": "#800080",   # Purple
    "structural": "#ff00ff", # Magenta
}

# Hazard icons (emoji for simplicity)
HAZARD_ICONS = {
    "flood": "🌊",
    "fire": "🔥",
    "debris": "🪨",
    "crowd": "👥",
    "traffic": "🚗",
    "landslide": "⛰️",
    "chemical": "☣️",
    "structural": "🏚️",
}

# ──────────────────────────────────────────────
# SHELTER TYPES & CAPACITY
# ──────────────────────────────────────────────
SHELTER_TYPES = {
    "school": {"capacity_multiplier": 1.0, "icon": "🏫", "priority": 1},
    "college": {"capacity_multiplier": 1.5, "icon": "🏛️", "priority": 2},
    "community_hall": {"capacity_multiplier": 0.8, "icon": "🏘️", "priority": 3},
    "religious": {"capacity_multiplier": 1.2, "icon": "🕌", "priority": 2},
    "hospital": {"capacity_multiplier": 0.5, "icon": "🏥", "priority": 1},  # Medical priority
    "stadium": {"capacity_multiplier": 3.0, "icon": "🏟️", "priority": 3},
    "govt_building": {"capacity_multiplier": 1.0, "icon": "🏢", "priority": 2},
}

# ──────────────────────────────────────────────
# ACCESSIBILITY — SIREN DETECTION & VIBRATION
# ──────────────────────────────────────────────
# Vibration patterns: (on_ms, off_ms, on_ms, off_ms, ...)
VIBRATION_PATTERNS = {
    "flood": [500, 200, 500, 200, 500],           # Long pulses — rising water
    "fire": [100, 50, 100, 50, 100, 50, 100],     # Rapid — urgency
    "evacuate": [300, 100, 300, 100, 300],        # Clear pattern — leave now
    "all_clear": [1000, 500, 1000],               # Long calm — safe
    "siren_generic": [200, 100, 200, 100, 200],   # Default
}

# Visual flash colors for deaf/HoH users
FLASH_COLORS = {
    "flood": "#0066ff",
    "fire": "#ff0000",
    "evacuate": "#ff8800",
    "all_clear": "#00ff00",
    "siren_generic": "#ffffff",
}

# ──────────────────────────────────────────────
# ROUTING SETTINGS
# ──────────────────────────────────────────────
# Grid resolution for A* (meters per cell) — lower = more precise, slower
GRID_RESOLUTION_M = 50

# Max search radius from start/end (km)
MAX_ROUTE_RADIUS_KM = 25

# Penalty for crossing hazard zones (added to distance cost)
HAZARD_CROSSING_PENALTY = 1000  # meters equivalent

# ──────────────────────────────────────────────
# OFFLINE MODE
# ──────────────────────────────────────────────
OFFLINE_MODE = os.getenv("OFFLINE_MODE", "true").lower() == "true"

# Path to pre-downloaded map tiles (MBTiles format)
OFFLINE_TILES_PATH = Path("src/data/sample_data/amritsar_tiles.mbtiles")

# ──────────────────────────────────────────────
# API KEYS (from .env)
# ──────────────────────────────────────────────
ORS_API_KEY = os.getenv("ORS_API_KEY", "")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")

# ──────────────────────────────────────────────
# APP SETTINGS
# ──────────────────────────────────────────────
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
APP_VERSION = "1.0.0-hackathon"
DEFAULT_LANGUAGE = "en"  # Add "hi", "pa" later

# File paths
DATA_DIR = Path("src/data/sample_data")
SHELTERS_CSV = DATA_DIR / "shelters.csv"
HAZARDS_CSV = DATA_DIR / "hazards.csv"

# ──────────────────────────────────────────────
# FAMILY/GROUP SETTINGS
# ──────────────────────────────────────────────
GROUP_CODE_LENGTH = 6
LOCATION_SHARE_INTERVAL_SEC = 30
MEETUP_POINT_BUFFER_M = 200  # Radius around calculated meetup point
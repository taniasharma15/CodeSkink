"""
LifeLine Navigator — Utility Functions
Helpers for formatting, validation, geospatial ops.
"""
import re
import hashlib
from typing import Tuple, Optional, List
from datetime import datetime
from haversine import haversine, Unit
from src.config import AMRITSAR_BOUNDS


def format_distance(meters: float) -> str:
    """Format distance for display."""
    if meters < 1000:
        return f"{meters:.0f} m"
    return f"{meters/1000:.1f} km"


def format_duration(minutes: float) -> str:
    """Format duration for display."""
    if minutes < 60:
        return f"{minutes:.0f} min"
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours}h {mins}min"


def format_coordinates(lat: float, lon: float, precision: int = 6) -> str:
    """Format coordinates as string."""
    return f"{lat:.{precision}f}, {lon:.{precision}f}"


def parse_coordinates(coord_str: str) -> Optional[Tuple[float, float]]:
    """Parse 'lat, lon' string."""
    try:
        parts = coord_str.replace(" ", "").split(",")
        if len(parts) == 2:
            lat, lon = float(parts[0]), float(parts[1])
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return lat, lon
    except (ValueError, IndexError):
        pass
    return None


def is_within_bounds(lat: float, lon: float, bounds: dict = None) -> bool:
    """Check if coordinates within city bounds."""
    b = bounds or AMRITSAR_BOUNDS
    return (b["min_lat"] <= lat <= b["max_lat"] and
            b["min_lon"] <= lon <= b["max_lon"])


def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate initial bearing from point 1 to point 2 (degrees)."""
    lat1, lon1, lat2, lon2 = map(__import__('math').radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    x = __import__('math').sin(dlon) * __import__('math').cos(lat2)
    y = __import__('math').cos(lat1) * __import__('math').sin(lat2) - \
        __import__('math').sin(lat1) * __import__('math').cos(lat2) * __import__('math').cos(dlon)
    bearing = __import__('math').atan2(x, y)
    return (__import__('math').degrees(bearing) + 360) % 360


def bearing_to_compass(bearing: float) -> str:
    """Convert bearing to compass direction."""
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    idx = round(bearing / 45) % 8
    return directions[idx]


def generate_id(prefix: str = "", length: int = 8) -> str:
    """Generate short unique ID."""
    import uuid
    uid = uuid.uuid4().hex[:length]
    return f"{prefix}{uid}" if prefix else uid


def hash_string(s: str, length: int = 12) -> str:
    """Short hash for deduplication."""
    return hashlib.md5(s.encode()).hexdigest()[:length]


def validate_phone_indian(phone: str) -> bool:
    """Validate Indian phone number format."""
    # Accept: +91XXXXXXXXXX, 91XXXXXXXXXX, XXXXXXXXXX, 0XXXXXXXXXX
    pattern = r"^(\+91|91|0)?[6-9]\d{9}$"
    return bool(re.match(pattern, phone.replace(" ", "").replace("-", "")))


def sanitize_filename(name: str) -> str:
    """Sanitize string for safe filename."""
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)


def time_ago(dt: datetime) -> str:
    """Human-readable time difference."""
    now = datetime.utcnow()
    diff = now - dt
    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        return f"{int(seconds/60)} min ago"
    elif seconds < 86400:
        return f"{int(seconds/3600)}h ago"
    else:
        return f"{int(seconds/86400)}d ago"


def interpolate_path(points: List[Tuple[float, float]], num_points: int) -> List[Tuple[float, float]]:
    """Interpolate path to have exactly num_points."""
    if len(points) < 2:
        return points

    # Calculate cumulative distances
    distances = [0.0]
    for i in range(1, len(points)):
        d = haversine(points[i-1], points[i], unit=Unit.METERS)
        distances.append(distances[-1] + d)

    total = distances[-1]
    if total == 0:
        return [points[0]] * num_points

    # Generate evenly spaced points
    result = []
    for i in range(num_points):
        target_dist = total * i / (num_points - 1)
        # Find segment
        for j in range(1, len(distances)):
            if distances[j] >= target_dist:
                t = (target_dist - distances[j-1]) / (distances[j] - distances[j-1])
                lat = points[j-1][0] + t * (points[j][0] - points[j-1][0])
                lon = points[j-1][1] + t * (points[j][1] - points[j-1][1])
                result.append((lat, lon))
                break
    return result


def grid_to_bounds(row: int, col: int, meta: dict) -> Tuple[float, float, float, float]:
    """Convert grid cell to lat/lon bounds (min_lat, min_lon, max_lat, max_lon)."""
    lat_step = meta["lat_step"]
    lon_step = meta["lon_step"]
    bounds = meta["bounds"]

    min_lat = bounds["min_lat"] + row * lat_step
    max_lat = min_lat + lat_step
    min_lon = bounds["min_lon"] + col * lon_step
    max_lon = min_lon + lon_step

    return min_lat, min_lon, max_lat, max_lon


# Color utilities for UI
def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    """Convert hex to rgba string."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def get_contrast_color(hex_color: str) -> str:
    """Get black or white for text on colored background."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    # Luminance
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#000000" if luminance > 0.5 else "#ffffff"
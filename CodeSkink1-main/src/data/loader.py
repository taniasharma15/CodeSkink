"""
LifeLine Navigator — Data Loading & Preprocessing
Loads shelters, hazards, and prepares data for routing/UI.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from src.config import (
    DATA_DIR, SHELTERS_CSV, HAZARDS_CSV,
    SHELTER_TYPES, HAZARD_WEIGHTS, HAZARD_COLORS, HAZARD_ICONS,
    AMRITSAR_BOUNDS
)


class DataLoader:
    """Handles loading and preprocessing of all static/dynamic data."""

    def __init__(self):
        self._shelters_df: Optional[pd.DataFrame] = None
        self._hazards_df: Optional[pd.DataFrame] = None
        self._shelter_cache: Dict = {}
        self._hazard_cache: Dict = {}

    # ──────────────────────────────────────────────
    # SHELTERS
    # ──────────────────────────────────────────────
    def load_shelters(self, force_reload: bool = False) -> pd.DataFrame:
        """Load shelters CSV with computed fields."""
        if self._shelters_df is not None and not force_reload:
            return self._shelters_df

        if not SHELTERS_CSV.exists():
            raise FileNotFoundError(f"Shelters file not found: {SHELTERS_CSV}")

        df = pd.read_csv(SHELTERS_CSV)

        # Validate required columns
        required = ["id", "name", "type", "latitude", "longitude", "capacity"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Shelters CSV missing columns: {missing}")

        # Add computed fields
        df["type_info"] = df["type"].map(SHELTER_TYPES)
        df["icon"] = df["type"].map(lambda t: SHELTER_TYPES.get(t, {}).get("icon", "🏠"))
        df["priority"] = df["type"].map(lambda t: SHELTER_TYPES.get(t, {}).get("priority", 3))
        df["effective_capacity"] = df.apply(
            lambda row: int(row["capacity"] * row["type_info"].get("capacity_multiplier", 1.0))
            if isinstance(row["type_info"], dict) else row["capacity"],
            axis=1
        )

        # Filter to city bounds
        df = df[
            (df["latitude"] >= AMRITSAR_BOUNDS["min_lat"]) &
            (df["latitude"] <= AMRITSAR_BOUNDS["max_lat"]) &
            (df["longitude"] >= AMRITSAR_BOUNDS["min_lon"]) &
            (df["longitude"] <= AMRITSAR_BOUNDS["max_lon"])
        ].copy()

        # Sort by priority (medical first), then capacity
        df = df.sort_values(["priority", "effective_capacity"], ascending=[True, False])

        self._shelters_df = df.reset_index(drop=True)
        return self._shelters_df

    def get_shelters_geojson(self) -> Dict:
        """Convert shelters to GeoJSON for folium mapping."""
        df = self.load_shelters()
        features = []
        for _, row in df.iterrows():
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row["longitude"], row["latitude"]]
                },
                "properties": {
                    "id": row["id"],
                    "name": row["name"],
                    "type": row["type"],
                    "icon": row["icon"],
                    "capacity": row["capacity"],
                    "effective_capacity": row["effective_capacity"],
                    "contact_person": row.get("contact_person", ""),
                    "contact_phone": row.get("contact_phone", ""),
                    "address": row.get("address", ""),
                    "facilities": row.get("facilities", ""),
                    "notes": row.get("notes", ""),
                    "priority": row["priority"]
                }
            })
        return {"type": "FeatureCollection", "features": features}

    def get_nearest_shelters(
        self, lat: float, lon: float, k: int = 5, hazard_filter: bool = True
    ) -> List[Dict]:
        """Find k nearest shelters, optionally filtering by active hazards."""
        from haversine import haversine, Unit

        df = self.load_shelters()
        if df.empty:
            return []

        # Calculate distances
        df = df.copy()
        df["distance_km"] = df.apply(
            lambda r: haversine((lat, lon), (r["latitude"], r["longitude"]), unit=Unit.KILOMETERS),
            axis=1
        )

        # TODO: Filter shelters inside active hazard zones when hazard_filter=True

        nearest = df.nsmallest(k, "distance_km")
        return nearest.to_dict("records")

    # ──────────────────────────────────────────────
    # HAZARDS
    # ──────────────────────────────────────────────
    def load_hazards(self, force_reload: bool = False, active_only: bool = True) -> pd.DataFrame:
        """Load hazards CSV with computed fields."""
        if self._hazards_df is not None and not force_reload:
            df = self._hazards_df
        else:
            if not HAZARDS_CSV.exists():
                # Return empty dataframe with correct structure
                return pd.DataFrame(columns=[
                    "id", "type", "latitude", "longitude", "radius_m",
                    "severity", "reported_at", "reported_by", "status", "description",
                    "weight", "color", "icon"
                ])

            df = pd.read_csv(HAZARDS_CSV)
            self._hazards_df = df

        # Add computed fields
        df = df.copy()
        df["weight"] = df["type"].map(HAZARD_WEIGHTS).fillna(1.0)
        df["color"] = df["type"].map(HAZARD_COLORS).fillna("#888888")
        df["icon"] = df["type"].map(HAZARD_ICONS).fillna("⚠️")

        # Parse timestamps
        if "reported_at" in df.columns:
            df["reported_at"] = pd.to_datetime(df["reported_at"], errors="coerce")

        if active_only:
            df = df[df["status"] == "active"].copy()

        # Filter to city bounds
        df = df[
            (df["latitude"] >= AMRITSAR_BOUNDS["min_lat"]) &
            (df["latitude"] <= AMRITSAR_BOUNDS["max_lat"]) &
            (df["longitude"] >= AMRITSAR_BOUNDS["min_lon"]) &
            (df["longitude"] <= AMRITSAR_BOUNDS["max_lon"])
        ]

        return df.reset_index(drop=True)

    def get_hazards_geojson(self, active_only: bool = True) -> Dict:
        """Convert hazards to GeoJSON circles for folium."""
        df = self.load_hazards(active_only=active_only)
        features = []
        for _, row in df.iterrows():
            # Create circle approximation (simplified as point with radius property)
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row["longitude"], row["latitude"]]
                },
                "properties": {
                    "id": row["id"],
                    "type": row["type"],
                    "radius_m": row["radius_m"],
                    "severity": row["severity"],
                    "weight": row["weight"],
                    "color": row["color"],
                    "icon": row["icon"],
                    "description": row.get("description", ""),
                    "reported_at": str(row.get("reported_at", "")),
                    "status": row.get("status", "active")
                }
            })
        return {"type": "FeatureCollection", "features": features}

    def get_hazard_grid(self, resolution_m: int = 50) -> Tuple[np.ndarray, Dict]:
        """
        Create a 2D hazard cost grid for A* routing.
        Returns (grid, metadata) where grid[y, x] = hazard cost multiplier.
        """
        bounds = AMRITSAR_BOUNDS
        lat_step = resolution_m / 111000  # ~111km per degree latitude
        lon_step = resolution_m / (111000 * np.cos(np.radians((bounds["min_lat"] + bounds["max_lat"]) / 2)))

        n_rows = int((bounds["max_lat"] - bounds["min_lat"]) / lat_step) + 1
        n_cols = int((bounds["max_lon"] - bounds["min_lon"]) / lon_step) + 1

        # Base grid = 1.0 (normal cost)
        grid = np.ones((n_rows, n_cols), dtype=np.float32)

        hazards = self.load_hazards(active_only=True)
        if hazards.empty:
            return grid, {"bounds": bounds, "lat_step": lat_step, "lon_step": lon_step}

        # For each hazard, increase cost in affected cells
        for _, haz in hazards.iterrows():
            weight = haz["weight"]
            radius_cells = max(1, int(haz["radius_m"] / resolution_m))

            # Convert hazard center to grid coordinates
            haz_row = int((haz["latitude"] - bounds["min_lat"]) / lat_step)
            haz_col = int((haz["longitude"] - bounds["min_lon"]) / lon_step)

            # Apply circular penalty
            r_min = max(0, haz_row - radius_cells)
            r_max = min(n_rows, haz_row + radius_cells + 1)
            c_min = max(0, haz_col - radius_cells)
            c_max = min(n_cols, haz_col + radius_cells + 1)

            for r in range(r_min, r_max):
                for c in range(c_min, c_max):
                    dr = r - haz_row
                    dc = c - haz_col
                    dist_cells = np.sqrt(dr*dr + dc*dc)
                    if dist_cells <= radius_cells:
                        # Gradient penalty: highest at center, fading at edge
                        penalty = weight * (1.0 - dist_cells / radius_cells) * 0.5 + weight * 0.5
                        grid[r, c] = max(grid[r, c], 1.0 + penalty)

        metadata = {
            "bounds": bounds,
            "lat_step": lat_step,
            "lon_step": lon_step,
            "n_rows": n_rows,
            "n_cols": n_cols,
            "resolution_m": resolution_m
        }
        return grid, metadata

    def latlon_to_grid(self, lat: float, lon: float, metadata: Dict) -> Tuple[int, int]:
        """Convert lat/lon to grid coordinates."""
        bounds = metadata["bounds"]
        lat_step = metadata["lat_step"]
        lon_step = metadata["lon_step"]
        row = int((lat - bounds["min_lat"]) / lat_step)
        col = int((lon - bounds["min_lon"]) / lon_step)
        # Clamp
        row = max(0, min(metadata["n_rows"] - 1, row))
        col = max(0, min(metadata["n_cols"] - 1, col))
        return row, col

    def grid_to_latlon(self, row: int, col: int, metadata: Dict) -> Tuple[float, float]:
        """Convert grid coordinates to lat/lon (center of cell)."""
        bounds = metadata["bounds"]
        lat_step = metadata["lat_step"]
        lon_step = metadata["lon_step"]
        lat = bounds["min_lat"] + (row + 0.5) * lat_step
        lon = bounds["min_lon"] + (col + 0.5) * lon_step
        return lat, lon


# Singleton instance
_data_loader = None

def get_data_loader() -> DataLoader:
    global _data_loader
    if _data_loader is None:
        _data_loader = DataLoader()
    return _data_loader
"""
LifeLine Navigator — Core Routing Engine
Multi-hazard A* routing with offline-first design.
Manual implementation (not an OSRM wrapper) — this is your "manual work" showcase.
"""
import heapq
import math
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass, field
from src.config import (
    AMRITSAR_BOUNDS, GRID_RESOLUTION_M, MAX_ROUTE_RADIUS_KM,
    HAZARD_CROSSING_PENALTY, HAZARD_WEIGHTS
)
from src.data.loader import get_data_loader
from src.api.schemas import Coordinates, RoutePoint, RouteResponse, RouteRequest


@dataclass(order=True)
class AStarNode:
    """A* search node with f-score as priority."""
    f_score: float
    g_score: float = field(compare=False)
    row: int = field(compare=False)
    col: int = field(compare=False)
    parent: Optional['AStarNode'] = field(default=None, compare=False)
    hazard_cost: float = field(default=1.0, compare=False)


class RoutingEngine:
    """
    Custom A* routing on a hazard-weighted grid.
    This is the core algorithm — manually implemented, not a wrapper.
    """

    def __init__(self):
        self.loader = get_data_loader()
        self._grid: Optional[np.ndarray] = None
        self._grid_meta: Optional[Dict] = None
        self._grid_version: int = 0

    def _ensure_grid_fresh(self):
        """Reload hazard grid if hazards have changed."""
        hazards_df = self.loader.load_hazards()
        current_version = len(hazards_df)  # Simple versioning
        if self._grid is None or current_version != self._grid_version:
            self._grid, self._grid_meta = self.loader.get_hazard_grid(GRID_RESOLUTION_M)
            self._grid_version = current_version

    def _heuristic(self, row1: int, col1: int, row2: int, col2: int) -> float:
        """Octile distance heuristic (good for 8-directional movement)."""
        dr = abs(row1 - row2)
        dc = abs(col1 - col2)
        return (dr + dc) + (math.sqrt(2) - 2) * min(dr, dc)

    def _get_neighbors(self, row: int, col: int, meta: Dict) -> List[Tuple[int, int, float]]:
        """Get 8-connected neighbors with movement costs."""
        n_rows, n_cols = meta["n_rows"], meta["n_cols"]
        neighbors = []

        # 8 directions: (d_row, d_col, base_cost)
        directions = [
            (-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),  # Cardinal
            (-1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)),           # Diagonal
            (1, -1, math.sqrt(2)), (1, 1, math.sqrt(2)),
        ]

        for dr, dc, base_cost in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < n_rows and 0 <= nc < n_cols:
                # Cost = base movement cost * hazard multiplier at target cell
                hazard_mult = self._grid[nr, nc]
                neighbors.append((nr, nc, base_cost * hazard_mult))

        return neighbors

    def _reconstruct_path(self, node: AStarNode, meta: Dict) -> List[RoutePoint]:
        """Reconstruct path from goal node to start."""
        path = []
        current = node
        while current is not None:
            lat, lon = self.loader.grid_to_latlon(current.row, current.col, meta)
            path.append(RoutePoint(
                latitude=lat,
                longitude=lon,
                hazard_cost=current.hazard_cost,
                is_hazard_zone=current.hazard_cost > 1.5
            ))
            current = current.parent
        path.reverse()
        return path

    def _calculate_distance_km(self, path: List[RoutePoint]) -> float:
        """Calculate total path distance in km using haversine."""
        from haversine import haversine, Unit
        if len(path) < 2:
            return 0.0
        total = 0.0
        for i in range(len(path) - 1):
            total += haversine(
                (path[i].latitude, path[i].longitude),
                (path[i+1].latitude, path[i+1].longitude),
                unit=Unit.KILOMETERS
            )
        return total

    def find_route(self, request: RouteRequest) -> RouteResponse:
        """
        Main routing entry point.
        Returns RouteResponse with path, distance, warnings.
        """
        self._ensure_grid_fresh()
        meta = self._grid_meta

        # Convert start/end to grid coordinates
        start_row, start_col = self.loader.latlon_to_grid(
            request.start.latitude, request.start.longitude, meta
        )
        goal_row, goal_col = self.loader.latlon_to_grid(
            request.end.latitude, request.end.longitude, meta
        )

        # Check if start/goal are in bounds
        n_rows, n_cols = meta["n_rows"], meta["n_cols"]
        if not (0 <= start_row < n_rows and 0 <= start_col < n_cols):
            return RouteResponse(
                success=False,
                message="Start location outside coverage area"
            )
        if not (0 <= goal_row < n_rows and 0 <= goal_col < n_cols):
            return RouteResponse(
                success=False,
                message="Destination outside coverage area"
            )

        # Quick check: direct distance vs max radius
        from haversine import haversine, Unit
        direct_km = haversine(
            (request.start.latitude, request.start.longitude),
            (request.end.latitude, request.end.longitude),
            unit=Unit.KILOMETERS
        )
        if direct_km > MAX_ROUTE_RADIUS_KM:
            return RouteResponse(
                success=False,
                message=f"Route too long ({direct_km:.1f}km > {MAX_ROUTE_RADIUS_KM}km max)"
            )

        # A* Search
        open_set = []
        closed_set = set()
        g_scores = {}

        start_node = AStarNode(
            f_score=0,
            g_score=0,
            row=start_row,
            col=start_col,
            hazard_cost=self._grid[start_row, start_col]
        )
        start_node.f_score = self._heuristic(start_row, start_col, goal_row, goal_col)
        heapq.heappush(open_set, start_node)
        g_scores[(start_row, start_col)] = 0.0

        max_iterations = n_rows * n_cols * 2  # Safety limit
        iterations = 0

        while open_set and iterations < max_iterations:
            iterations += 1
            current = heapq.heappop(open_set)

            if (current.row, current.col) in closed_set:
                continue

            if current.row == goal_row and current.col == goal_col:
                # Goal reached
                path = self._reconstruct_path(current, meta)
                distance_km = self._calculate_distance_km(path)

                # Count hazard zones crossed
                hazard_crossings = sum(1 for p in path if p.is_hazard_zone)

                # Estimate time (walking ~5 km/h, adjust for vehicle)
                speed_kmh = {"foot": 5, "bicycle": 15, "car": 30, "motorcycle": 25}
                speed = speed_kmh.get(request.vehicle_type, 5)
                # Slow down in hazard zones
                hazard_slowdown = 1.0 + (hazard_crossings * 0.3)
                time_min = (distance_km / speed) * 60 * hazard_slowdown

                warnings = []
                if hazard_crossings > 0:
                    warnings.append(f"Route crosses {hazard_crossings} hazard zone(s)")
                if distance_km > direct_km * request.max_detour_factor:
                    warnings.append("Route significantly longer than direct path")

                return RouteResponse(
                    success=True,
                    route=path,
                    total_distance_km=round(distance_km, 2),
                    estimated_time_min=round(time_min, 1),
                    hazard_zones_crossed=hazard_crossings,
                    warnings=warnings,
                    fallback_used=False
                )

            closed_set.add((current.row, current.col))

            # Explore neighbors
            for nr, nc, move_cost in self._get_neighbors(current.row, current.col, meta):
                if (nr, nc) in closed_set:
                    continue

                tentative_g = current.g_score + move_cost * GRID_RESOLUTION_M / 1000.0  # km

                if (nr, nc) not in g_scores or tentative_g < g_scores[(nr, nc)]:
                    g_scores[(nr, nc)] = tentative_g
                    h = self._heuristic(nr, nc, goal_row, goal_col)
                    neighbor_node = AStarNode(
                        f_score=tentative_g + h,
                        g_score=tentative_g,
                        row=nr,
                        col=nc,
                        parent=current,
                        hazard_cost=self._grid[nr, nc]
                    )
                    heapq.heappush(open_set, neighbor_node)

        # No path found - fallback to direct line (emergency)
        return self._fallback_route(request, direct_km)

    def _fallback_route(self, request: RouteRequest, direct_km: float) -> RouteResponse:
        """Emergency fallback: straight line with hazard warnings."""
        # Sample points along direct line
        n_points = max(10, int(direct_km * 1000 / GRID_RESOLUTION_M))
        path = []
        hazard_crossings = 0

        for i in range(n_points + 1):
            t = i / n_points
            lat = request.start.latitude + t * (request.end.latitude - request.start.latitude)
            lon = request.start.longitude + t * (request.end.longitude - request.start.longitude)

            # Check hazard at this point
            row, col = self.loader.latlon_to_grid(lat, lon, self._grid_meta)
            hazard_cost = self._grid[row, col]
            is_hazard = hazard_cost > 1.5

            if is_hazard:
                hazard_crossings += 1

            path.append(RoutePoint(
                latitude=lat,
                longitude=lon,
                hazard_cost=hazard_cost,
                is_hazard_zone=is_hazard
            ))

        warnings = ["⚠️ FALLBACK: No safe path found — direct route shown"]
        if hazard_crossings > 0:
            warnings.append(f"Direct route crosses {hazard_crossings} hazard zone(s)")

        return RouteResponse(
            success=True,
            route=path,
            total_distance_km=round(direct_km, 2),
            estimated_time_min=round(direct_km / 5 * 60, 1),  # Walking speed
            hazard_zones_crossed=hazard_crossings,
            warnings=warnings,
            fallback_used=True,
            message="Using emergency fallback route — proceed with extreme caution"
        )


# ──────────────────────────────────────────────
# SINGLETON & HELPERS
# ──────────────────────────────────────────────
_routing_engine = None

def get_routing_engine() -> RoutingEngine:
    global _routing_engine
    if _routing_engine is None:
        _routing_engine = RoutingEngine()
    return _routing_engine


def calculate_route(request: RouteRequest) -> RouteResponse:
    """Convenience function for API layer."""
    engine = get_routing_engine()
    return engine.find_route(request)


def get_safe_meetup_point(member_locations: List[Coordinates]) -> Optional[Coordinates]:
    """
    Calculate geometric median (approximate) as meetup point.
    Then find nearest safe shelter.
    """
    if not member_locations:
        return None

    if len(member_locations) == 1:
        return member_locations[0]

    # Geometric median approximation (Weiszfeld's algorithm)
    # Start with centroid
    lat = sum(m.latitude for m in member_locations) / len(member_locations)
    lon = sum(m.longitude for m in member_locations) / len(member_locations)

    for _ in range(10):  # Iterate
        num_lat, num_lon, denom = 0.0, 0.0, 0.0
        for m in member_locations:
            from haversine import haversine, Unit
            d = haversine((lat, lon), (m.latitude, m.longitude), unit=Unit.KILOMETERS)
            if d < 0.001:  # Avoid division by zero
                continue
            w = 1.0 / d
            num_lat += m.latitude * w
            num_lon += m.longitude * w
            denom += w
        if denom > 0:
            lat, lon = num_lat / denom, num_lon / denom

    # Find nearest shelter to this point
    loader = get_data_loader()
    shelters = loader.get_nearest_shelters(lat, lon, k=1)
    if shelters:
        return Coordinates(latitude=shelters[0]["latitude"], longitude=shelters[0]["longitude"])

    return Coordinates(latitude=lat, longitude=lon)
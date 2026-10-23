"""
LifeLine Navigator — Business Logic Services
Shelter management, family groups, hazard monitoring, offline sync.
"""
import uuid
import time
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from threading import Lock
from src.config import (
    GROUP_CODE_LENGTH, LOCATION_SHARE_INTERVAL_SEC,
    MEETUP_POINT_BUFFER_M, AMRITSAR_BOUNDS
)
from src.data.loader import get_data_loader
from src.api.routing import get_safe_meetup_point
from src.api.schemas import (
    Coordinates, Shelter, Hazard, FamilyGroup, FamilyMember,
    MeetupPointResponse, RouteRequest, RouteResponse,
    ShelterSearchRequest, FamilyGroupCreate, FamilyGroupJoin,
    LocationUpdate, AlertTrigger, OfflineMapStatus, AppStatus
)
from src.api.routing import calculate_route


@dataclass
class FamilyGroupState:
    """In-memory family group state (replace with Redis/DB in production)."""
    group_code: str
    creator_id: str
    members: Dict[str, FamilyMember] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    meetup_point: Optional[Coordinates] = None
    is_active: bool = True
    last_meetup_update: Optional[datetime] = None


class ShelterService:
    """Shelter discovery and management."""

    def __init__(self):
        self.loader = get_data_loader()

    def search_shelters(self, request: ShelterSearchRequest) -> List[Shelter]:
        """Find shelters near location with filters."""
        shelters_data = self.loader.get_nearest_shelters(
            request.location.latitude,
            request.location.longitude,
            k=request.limit
        )

        results = []
        for s in shelters_data:
            if request.min_capacity and s["effective_capacity"] < request.min_capacity:
                continue
            if request.shelter_types and s["type"] not in [t.value for t in request.shelter_types]:
                continue

            results.append(Shelter(
                id=s["id"],
                name=s["name"],
                type=s["type"],
                latitude=s["latitude"],
                longitude=s["longitude"],
                capacity=s["capacity"],
                effective_capacity=s["effective_capacity"],
                contact_person=s.get("contact_person", ""),
                contact_phone=s.get("contact_phone", ""),
                address=s.get("address", ""),
                facilities=s.get("facilities", ""),
                notes=s.get("notes", ""),
                icon=s.get("icon", "🏠"),
                priority=s.get("priority", 3),
                distance_km=s.get("distance_km")
            ))
        return results

    def get_shelter_by_id(self, shelter_id: str) -> Optional[Shelter]:
        """Get single shelter by ID."""
        df = self.loader.load_shelters()
        row = df[df["id"] == shelter_id]
        if row.empty:
            return None
        r = row.iloc[0]
        return Shelter(
            id=r["id"], name=r["name"], type=r["type"],
            latitude=r["latitude"], longitude=r["longitude"],
            capacity=r["capacity"], effective_capacity=r["effective_capacity"],
            contact_person=r.get("contact_person", ""),
            contact_phone=r.get("contact_phone", ""),
            address=r.get("address", ""),
            facilities=r.get("facilities", ""),
            notes=r.get("notes", ""),
            icon=r.get("icon", "🏠"), priority=r.get("priority", 3)
        )

    def get_all_shelters_geojson(self) -> Dict:
        return self.loader.get_shelters_geojson()


class HazardService:
    """Hazard monitoring and management."""

    def __init__(self):
        self.loader = get_data_loader()

    def get_active_hazards(self) -> List[Hazard]:
        """Get all active hazards."""
        df = self.loader.load_hazards(active_only=True)
        hazards = []
        for _, row in df.iterrows():
            hazards.append(Hazard(
                id=row["id"],
                type=row["type"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                radius_m=row["radius_m"],
                severity=row["severity"],
                reported_at=row["reported_at"],
                reported_by=row["reported_by"],
                status=row["status"],
                description=row.get("description", ""),
                weight=row["weight"],
                color=row["color"],
                icon=row["icon"]
            ))
        return hazards

    def get_hazards_geojson(self) -> Dict:
        return self.loader.get_hazards_geojson(active_only=True)

    def add_hazard(self, hazard: Hazard) -> bool:
        """Add new hazard report (in production: write to DB)."""
        # For hackathon: append to CSV
        import pandas as pd
        new_row = pd.DataFrame([{
            "id": hazard.id,
            "type": hazard.type.value,
            "latitude": hazard.latitude,
            "longitude": hazard.longitude,
            "radius_m": hazard.radius_m,
            "severity": hazard.severity.value,
            "reported_at": hazard.reported_at.isoformat(),
            "reported_by": hazard.reported_by,
            "status": hazard.status.value,
            "description": hazard.description
        }])
        new_row.to_csv("src/data/sample_data/hazards.csv", mode="a", header=False, index=False)
        self.loader.load_hazards(force_reload=True)
        return True

    def clear_hazard(self, hazard_id: str) -> bool:
        """Mark hazard as cleared."""
        import pandas as pd
        df = pd.read_csv("src/data/sample_data/hazards.csv")
        df.loc[df["id"] == hazard_id, "status"] = "cleared"
        df.to_csv("src/data/sample_data/hazards.csv", index=False)
        self.loader.load_hazards(force_reload=True)
        return True


class FamilyService:
    """Family/group location sharing and coordination."""

    def __init__(self):
        self.groups: Dict[str, FamilyGroupState] = {}
        self.member_to_group: Dict[str, str] = {}  # member_id -> group_code
        self.lock = Lock()

    def _generate_group_code(self) -> str:
        """Generate unique 6-char group code."""
        chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # No confusing chars
        while True:
            code = "".join(uuid.uuid4().hex[i % 32] for i in range(GROUP_CODE_LENGTH)).upper()
            code = "".join(c for c in code if c in chars)[:GROUP_CODE_LENGTH]
            if code not in self.groups:
                return code

    def create_group(self, request: FamilyGroupCreate) -> FamilyGroup:
        """Create new family group."""
        with self.lock:
            group_code = self._generate_group_code()
            creator_id = str(uuid.uuid4())[:8]

            creator = FamilyMember(
                member_id=creator_id,
                name=request.creator_name,
                phone=request.creator_phone,
                is_creator=True
            )

            group = FamilyGroupState(
                group_code=group_code,
                creator_id=creator_id,
                members={creator_id: creator}
            )
            self.groups[group_code] = group
            self.member_to_group[creator_id] = group_code

            return self._to_response(group)

    def join_group(self, request: FamilyGroupJoin) -> FamilyGroup:
        """Join existing group."""
        with self.lock:
            group = self.groups.get(request.group_code.upper())
            if not group or not group.is_active:
                raise ValueError("Invalid or inactive group code")

            member_id = str(uuid.uuid4())[:8]
            member = FamilyMember(
                member_id=member_id,
                name=request.member_name,
                phone=request.member_phone
            )
            group.members[member_id] = member
            self.member_to_group[member_id] = request.group_code.upper()

            return self._to_response(group)

    def leave_group(self, group_code: str, member_id: str) -> bool:
        """Leave group."""
        with self.lock:
            group = self.groups.get(group_code.upper())
            if not group:
                return False
            if member_id in group.members:
                del group.members[member_id]
                self.member_to_group.pop(member_id, None)
                if not group.members:
                    group.is_active = False
                return True
            return False

    def update_location(self, update: LocationUpdate) -> FamilyGroup:
        """Update member location and recalculate meetup point."""
        with self.lock:
            group = self.groups.get(update.group_code.upper())
            if not group:
                raise ValueError("Group not found")

            member = group.members.get(update.member_id)
            if not member:
                raise ValueError("Member not found")

            member.latitude = update.latitude
            member.longitude = update.longitude
            member.last_update = update.timestamp
            member.battery_level = update.battery_level
            member.is_safe = update.is_safe

            # Recalculate meetup point if enough members have location
            locations = [
                Coordinates(latitude=m.latitude, longitude=m.longitude)
                for m in group.members.values()
                if m.latitude is not None and m.longitude is not None
            ]
            if len(locations) >= 2:
                meetup = get_safe_meetup_point(locations)
                if meetup:
                    group.meetup_point = meetup
                    group.last_meetup_update = datetime.utcnow()

            return self._to_response(group)

    def get_group(self, group_code: str) -> Optional[FamilyGroup]:
        with self.lock:
            group = self.groups.get(group_code.upper())
            return self._to_response(group) if group else None

    def get_meetup_point(self, group_code: str) -> Optional[MeetupPointResponse]:
        with self.lock:
            group = self.groups.get(group_code.upper())
            if not group or not group.meetup_point:
                return None

            # Calculate distances from each member
            distances = {}
            for m_id, member in group.members.items():
                if member.latitude and member.longitude:
                    from haversine import haversine, Unit
                    d = haversine(
                        (member.latitude, member.longitude),
                        (group.meetup_point.latitude, group.meetup_point.longitude),
                        unit=Unit.KILOMETERS
                    )
                    distances[m_id] = round(d, 2)

            return MeetupPointResponse(
                latitude=group.meetup_point.latitude,
                longitude=group.meetup_point.longitude,
                address=f"Near {self._get_nearby_landmark(group.meetup_point)}",
                distance_from_members=distances
            )

    def _get_nearby_landmark(self, coord: Coordinates) -> str:
        """Find nearest shelter/landmark for address."""
        shelters = self.loader.get_nearest_shelters(coord.latitude, coord.longitude, k=1)
        if shelters:
            return shelters[0]["name"]
        return "Unknown location"

    def _to_response(self, group: FamilyGroupState) -> FamilyGroup:
        return FamilyGroup(
            group_code=group.group_code,
            creator_id=group.creator_id,
            members=list(group.members.values()),
            created_at=group.created_at,
            meetup_point=group.meetup_point,
            is_active=group.is_active
        )


class RoutingService:
    """High-level routing service."""

    def __init__(self):
        pass

    def get_route(self, request: RouteRequest) -> RouteResponse:
        return calculate_route(request)


class OfflineService:
    """Offline map management."""

    def __init__(self):
        self.tiles_path = "src/data/sample_data/amritsar_tiles.mbtiles"

    def get_status(self) -> OfflineMapStatus:
        from pathlib import Path
        path = Path(self.tiles_path)
        return OfflineMapStatus(
            tiles_downloaded=path.exists(),
            tiles_path=self.tiles_path,
            coverage_bounds=AMRITSAR_BOUNDS,
            last_updated=datetime.fromtimestamp(path.stat().st_mtime) if path.exists() else None,
            size_mb=round(path.stat().st_size / (1024*1024), 1) if path.exists() else 0.0
        )

    def download_tiles(self, bounds: Dict = None) -> bool:
        """Placeholder for tile download logic (use MOBAC or similar offline)."""
        # In production: use map tile downloader
        # For hackathon: just create placeholder
        Path(self.tiles_path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.tiles_path).write_bytes(b"PLACEHOLDER_MBTILES_FILE")
        return True


class AppService:
    """Application-level status and health."""

    def __init__(self):
        self.shelter_service = ShelterService()
        self.hazard_service = HazardService()

    def get_status(self) -> AppStatus:
        shelters_df = self.shelter_service.loader.load_shelters()
        hazards = self.hazard_service.get_active_hazards()
        return AppStatus(
            version="1.0.0-hackathon",
            offline_mode=True,
            api_connected=False,  # Would check ORS/Weather APIs
            shelters_loaded=len(shelters_df),
            hazards_active=len(hazards),
            last_hazard_update=max([h.reported_at for h in hazards]) if hazards else None
        )


# ──────────────────────────────────────────────
# SINGLETONS
# ──────────────────────────────────────────────
_shelter_service = None
_hazard_service = None
_family_service = None
_routing_service = None
_offline_service = None
_app_service = None

def get_shelter_service() -> ShelterService:
    global _shelter_service
    if _shelter_service is None:
        _shelter_service = ShelterService()
    return _shelter_service

def get_hazard_service() -> HazardService:
    global _hazard_service
    if _hazard_service is None:
        _hazard_service = HazardService()
    return _hazard_service

def get_family_service() -> FamilyService:
    global _family_service
    if _family_service is None:
        _family_service = FamilyService()
    return _family_service

def get_routing_service() -> RoutingService:
    global _routing_service
    if _routing_service is None:
        _routing_service = RoutingService()
    return _routing_service

def get_offline_service() -> OfflineService:
    global _offline_service
    if _offline_service is None:
        _offline_service = OfflineService()
    return _offline_service

def get_app_service() -> AppService:
    global _app_service
    if _app_service is None:
        _app_service = AppService()
    return _app_service
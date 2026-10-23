"""
LifeLine Navigator — Pydantic Schemas
Request/Response models for API layer.
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum


# ──────────────────────────────────────────────
# ENUMS
# ──────────────────────────────────────────────
class HazardType(str, Enum):
    FLOOD = "flood"
    FIRE = "fire"
    DEBRIS = "debris"
    CROWD = "crowd"
    TRAFFIC = "traffic"
    LANDSLIDE = "landslide"
    CHEMICAL = "chemical"
    STRUCTURAL = "structural"


class HazardSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ShelterType(str, Enum):
    SCHOOL = "school"
    COLLEGE = "college"
    COMMUNITY_HALL = "community_hall"
    RELIGIOUS = "religious"
    HOSPITAL = "hospital"
    STADIUM = "stadium"
    GOVT_BUILDING = "govt_building"


class AlertType(str, Enum):
    FLOOD = "flood"
    FIRE = "fire"
    EVACUATE = "evacuate"
    ALL_CLEAR = "all_clear"
    SIREN_GENERIC = "siren_generic"


class HazardStatus(str, Enum):
    ACTIVE = "active"
    CLEARED = "cleared"
    PREDICTED = "predicted"


# ──────────────────────────────────────────────
# CORE MODELS
# ──────────────────────────────────────────────
class Coordinates(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    def to_tuple(self) -> tuple:
        return (self.latitude, self.longitude)


class Hazard(BaseModel):
    id: str
    type: HazardType
    latitude: float
    longitude: float
    radius_m: float = Field(..., gt=0)
    severity: HazardSeverity
    reported_at: datetime
    reported_by: str
    status: HazardStatus = HazardStatus.ACTIVE
    description: str = ""
    weight: float = 1.0
    color: str = "#888888"
    icon: str = "⚠️"


class Shelter(BaseModel):
    id: str
    name: str
    type: ShelterType
    latitude: float
    longitude: float
    capacity: int = Field(..., gt=0)
    effective_capacity: int = Field(..., gt=0)
    contact_person: str = ""
    contact_phone: str = ""
    address: str = ""
    facilities: str = ""
    notes: str = ""
    icon: str = "🏠"
    priority: int = 3
    distance_km: Optional[float] = None


class RoutePoint(BaseModel):
    latitude: float
    longitude: float
    hazard_cost: float = 1.0
    is_hazard_zone: bool = False


class RouteResponse(BaseModel):
    success: bool
    route: List[RoutePoint] = []
    total_distance_km: float = 0.0
    estimated_time_min: float = 0.0
    hazard_zones_crossed: int = 0
    warnings: List[str] = []
    fallback_used: bool = False
    message: str = ""


# ──────────────────────────────────────────────
# REQUEST MODELS
# ──────────────────────────────────────────────
class RouteRequest(BaseModel):
    start: Coordinates
    end: Coordinates
    avoid_hazards: bool = True
    vehicle_type: Literal["foot", "bicycle", "car", "motorcycle"] = "foot"
    max_detour_factor: float = Field(2.0, ge=1.0, le=10.0)  # Max route length vs direct


class ShelterSearchRequest(BaseModel):
    location: Coordinates
    radius_km: float = Field(10.0, gt=0, le=50)
    min_capacity: int = 0
    shelter_types: Optional[List[ShelterType]] = None
    limit: int = Field(10, gt=0, le=50)


class FamilyGroupCreate(BaseModel):
    creator_name: str = Field(..., min_length=1, max_length=50)
    creator_phone: Optional[str] = None


class FamilyGroupJoin(BaseModel):
    group_code: str = Field(..., min_length=6, max_length=6)
    member_name: str = Field(..., min_length=1, max_length=50)
    member_phone: Optional[str] = None


class LocationUpdate(BaseModel):
    group_code: str
    member_id: str
    latitude: float
    longitude: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    battery_level: Optional[int] = Field(None, ge=0, le=100)
    is_safe: bool = True


class AlertTrigger(BaseModel):
    alert_type: AlertType
    location: Optional[Coordinates] = None
    message: str = ""
    target_group: Optional[str] = None  # group_code or "all"


# ──────────────────────────────────────────────
# RESPONSE MODELS
# ──────────────────────────────────────────────
class FamilyMember(BaseModel):
    member_id: str
    name: str
    phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    last_update: Optional[datetime] = None
    battery_level: Optional[int] = None
    is_safe: bool = True
    is_creator: bool = False


class FamilyGroup(BaseModel):
    group_code: str
    creator_id: str
    members: List[FamilyMember] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    meetup_point: Optional[Coordinates] = None
    is_active: bool = True


class MeetupPointResponse(BaseModel):
    latitude: float
    longitude: float
    address: str = ""
    distance_from_members: Dict[str, float] = {}  # member_id -> km


class OfflineMapStatus(BaseModel):
    tiles_downloaded: bool
    tiles_path: str
    coverage_bounds: Dict[str, float]
    last_updated: Optional[datetime] = None
    size_mb: float = 0.0


class AppStatus(BaseModel):
    version: str
    offline_mode: bool
    api_connected: bool
    shelters_loaded: int
    hazards_active: int
    last_hazard_update: Optional[datetime] = None


# ──────────────────────────────────────────────
# UTILITY
# ──────────────────────────────────────────────
class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None
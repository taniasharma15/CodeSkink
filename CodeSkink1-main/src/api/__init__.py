"""
LifeLine Navigator — API Package
"""
from src.api.schemas import *
from src.api.routing import RoutingEngine, calculate_route, get_safe_meetup_point
from src.api.alerts import AlertManager, SirenDetector, HapticFeedback, get_alert_manager
from src.api.services import (
    ShelterService, HazardService, FamilyService,
    RoutingService, OfflineService, AppService,
    get_shelter_service, get_hazard_service, get_family_service,
    get_routing_service, get_offline_service, get_app_service
)
from src.api.utils import *

__all__ = [
    # Schemas
    "Coordinates", "Hazard", "Shelter", "RoutePoint", "RouteResponse",
    "RouteRequest", "ShelterSearchRequest", "FamilyGroupCreate", "FamilyGroupJoin",
    "LocationUpdate", "AlertTrigger", "FamilyMember", "FamilyGroup",
    "MeetupPointResponse", "OfflineMapStatus", "AppStatus",
    "HazardType", "HazardSeverity", "ShelterType", "AlertType", "HazardStatus",
    # Routing
    "RoutingEngine", "calculate_route", "get_safe_meetup_point",
    # Alerts
    "AlertManager", "SirenDetector", "HapticFeedback", "get_alert_manager",
    # Services
    "ShelterService", "HazardService", "FamilyService",
    "RoutingService", "OfflineService", "AppService",
    "get_shelter_service", "get_hazard_service", "get_family_service",
    "get_routing_service", "get_offline_service", "get_app_service",
    # Utils
    "format_distance", "format_duration", "format_coordinates",
    "parse_coordinates", "is_within_bounds", "calculate_bearing",
    "bearing_to_compass", "generate_id", "hash_string",
    "validate_phone_indian", "sanitize_filename", "time_ago",
    "interpolate_path", "grid_to_bounds", "hex_to_rgba", "get_contrast_color",
]
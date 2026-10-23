# LifeLine Navigator API Documentation

This document describes the API endpoints and data models used in LifeLine Navigator.

## 📊 Data Models

### Coordinates
```python
class Coordinates(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
```

### Hazard
```python
class Hazard(BaseModel):
    id: str
    type: HazardType  # flood, fire, debris, crowd, traffic, landslide, chemical, structural
    latitude: float
    longitude: float
    radius_m: float
    severity: HazardSeverity  # low, medium, high, critical
    reported_at: datetime
    reported_by: str
    status: HazardStatus  # active, cleared, predicted
    description: str = ""
    weight: float = 1.0
    color: str = "#888888"
    icon: str = "⚠️"
```

### Shelter
```python
class Shelter(BaseModel):
    id: str
    name: str
    type: ShelterType  # school, college, community_hall, religious, hospital, stadium, govt_building
    latitude: float
    longitude: float
    capacity: int
    effective_capacity: int
    contact_person: str = ""
    contact_phone: str = ""
    address: str = ""
    facilities: str = ""
    notes: str = ""
    icon: str = "🏠"
    priority: int = 3
    distance_km: Optional[float] = None
```

## 🚗 Routing API

### RouteRequest
```python
class RouteRequest(BaseModel):
    start: Coordinates
    end: Coordinates
    avoid_hazards: bool = True
    vehicle_type: Literal["foot", "bicycle", "car", "motorcycle"] = "foot"
    max_detour_factor: float = Field(2.0, ge=1.0, le=10.0)
```

### RouteResponse
```python
class RouteResponse(BaseModel):
    success: bool
    route: List[RoutePoint] = []
    total_distance_km: float = 0.0
    estimated_time_min: float = 0.0
    hazard_zones_crossed: int = 0
    warnings: List[str] = []
    fallback_used: bool = False
    message: str = ""
```

## 👨‍👩‍👧‍👦 Family Tracking API

### FamilyGroupCreate
```python
class FamilyGroupCreate(BaseModel):
    creator_name: str = Field(..., min_length=1, max_length=50)
    creator_phone: Optional[str] = None
```

### FamilyGroupJoin
```python
class FamilyGroupJoin(BaseModel):
    group_code: str = Field(..., min_length=6, max_length=6)
    member_name: str = Field(..., min_length=1, max_length=50)
    member_phone: Optional[str] = None
```

### LocationUpdate
```python
class LocationUpdate(BaseModel):
    group_code: str
    member_id: str
    latitude: float
    longitude: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    battery_level: Optional[int] = Field(None, ge=0, le=100)
    is_safe: bool = True
```

## 🚨 Alert API

### AlertTrigger
```python
class AlertTrigger(BaseModel):
    alert_type: AlertType  # flood, fire, evacuate, all_clear, siren_generic
    location: Optional[Coordinates] = None
    message: str = ""
    target_group: Optional[str] = None
```

## 🔧 Service Functions

### Routing Services

```python
def calculate_route(request: RouteRequest) -> RouteResponse:
    """
    Calculate the safest route between two points.
    
    Args:
        request: Route request with start/end points and preferences
        
    Returns:
        RouteResponse with calculated path or error message
    """
    pass

def get_safe_meetup_point(member_locations: List[Coordinates]) -> Optional[Coordinates]:
    """
    Calculate optimal meetup point for family members.
    
    Args:
        member_locations: List of family member locations
        
    Returns:
        Optimal meetup coordinates or None if no locations provided
    """
    pass
```

### Data Services

```python
def load_shelters() -> pd.DataFrame:
    """
    Load shelter data from CSV.
    
    Returns:
        DataFrame with shelter information
    """
    pass

def load_hazards() -> pd.DataFrame:
    """
    Load hazard data from CSV.
    
    Returns:
        DataFrame with hazard information
    """
    pass

def get_nearest_shelters(latitude: float, longitude: float, 
                       radius_km: float = 10, limit: int = 10) -> List[Dict]:
    """
    Find nearest shelters to a location.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        radius_km: Search radius in kilometers
        limit: Maximum number of results
        
    Returns:
        List of nearby shelters with distance information
    """
    pass
```

### Alert Services

```python
def create_alert(alert_type: AlertType, location: Optional[Coordinates] = None,
                message: str = "", target_group: Optional[str] = None) -> bool:
    """
    Create and broadcast an alert.
    
    Args:
        alert_type: Type of alert
        location: Optional location for the alert
        message: Alert message
        target_group: Optional group code to target
        
    Returns:
        True if alert was created successfully
    """
    pass

def broadcast_to_group(group_code: str, alert: AlertTrigger) -> bool:
    """
    Broadcast an alert to a specific family group.
    
    Args:
        group_code: Family group code
        alert: Alert to broadcast
        
    Returns:
        True if broadcast successful
    """
    pass
```

## 📈 Response Formats

### Success Response
```json
{
    "success": true,
    "message": "Operation completed successfully",
    "data": {
        // Response-specific data
    }
}
```

### Error Response
```json
{
    "success": false,
    "error": "Error description",
    "details": {
        // Additional error details
    }
}
```

## 🔍 Error Handling

### Common Error Types

1. **ValidationError** - Invalid input data
   - Status: 400
   - When: Input doesn't match schema requirements

2. **NotFoundError** - Resource not found
   - Status: 404
   - When: Shelters, hazards, or groups don't exist

3. **RoutingError** - Route calculation failed
   - Status: 422
   - When: No safe path found or invalid coordinates

4. **ConfigurationError** - Configuration issue
   - Status: 500
   - When: Missing configuration or data files

### Error Response Example
```python
ErrorResponse(
    success=False,
    error="Invalid coordinates",
    details={
        "latitude": "Must be between -90 and 90",
        "longitude": "Must be between -180 and 180"
    }
)
```

## 🎯 Configuration

### Hazard Weights
Configure in `src/config.py`:
```python
HAZARD_WEIGHTS = {
    "flood": 10.0,       # Deep water - impassable
    "fire": 8.0,         # Active fire perimeter
    "debris": 5.0,       # Building collapse
    "crowd": 3.0,        # Protest, stampede risk
    "traffic": 2.0,      # Normal congestion
    "landslide": 9.0,    # Mountain areas
    "chemical": 10.0,    # Industrial hazard
    "structural": 7.0,   # Damaged buildings
}
```

### Map Configuration
```python
# City bounds
AMRITSAR_BOUNDS = {
    "min_lat": 31.55,
    "min_lon": 74.70,
    "max_lat": 31.75,
    "max_lon": 74.95,
}

# Map settings
MAP_CENTER = [31.6340, 74.8723]
MAP_ZOOM_START = 12
```

## 📝 Usage Examples

### Basic Route Calculation
```python
from src.api.schemas import RouteRequest, Coordinates
from src.api.routing import calculate_route

# Create route request
request = RouteRequest(
    start=Coordinates(latitude=31.634, longitude=74.872),
    end=Coordinates(latitude=31.650, longitude=74.890),
    vehicle_type="foot",
    avoid_hazards=True
)

# Calculate route
result = calculate_route(request)

if result.success:
    print(f"Distance: {result.total_distance_km} km")
    print(f"Time: {result.estimated_time_min} minutes")
    print(f"Hazard zones crossed: {result.hazard_zones_crossed}")
else:
    print(f"Error: {result.message}")
```

### Find Nearest Shelters
```python
from src.data.loader import get_data_loader

loader = get_data_loader()
shelters = loader.get_nearest_shelters(31.634, 74.872, radius_km=5, limit=5)

for shelter in shelters:
    print(f"{shelter['name']} - {shelter['distance_km']:.1f}km away")
```

### Create Family Group
```python
from src.api.services import create_family_group

# Create group
group = create_family_group(
    creator_name="John Doe",
    creator_phone="+919876543210"
)

print(f"Group created: {group['group_code']}")
```

---

This API documentation covers the core functionality of LifeLine Navigator. For more detailed implementation, refer to the source code in `src/api/`.
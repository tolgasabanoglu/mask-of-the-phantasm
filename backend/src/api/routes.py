from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

router = APIRouter()

# Request/Response models
class RouteRequest(BaseModel):
    distance: float  # in meters (e.g., 5000 for 5km)
    start_point: List[float]  # [longitude, latitude]
    start_location: Optional[str] = None  # e.g., "Mitte", "Kreuzberg"

class RouteResponse(BaseModel):
    route_id: str
    coordinates: List[List[float]]  # List of [lon, lat] pairs
    distance: float
    darkness_score: float  # 0-1 (higher = darker)
    greenness_score: float  # 0-1 (higher = greener)
    estimated_time: int  # in minutes

# Test endpoint - fetch NDVI for a point
class NDVIRequest(BaseModel):
    lat: float
    lon: float

@router.post("/test/ndvi")
async def test_ndvi(request: NDVIRequest):
    """
    Test endpoint to fetch NDVI for a single point.
    """
    from src.services.ndvi import ndvi_service
    
    try:
        ndvi_value = ndvi_service.get_ndvi_for_point(
            request.lat, 
            request.lon
        )
        
        return {
            "lat": request.lat,
            "lon": request.lon,
            "ndvi": ndvi_value,
            "interpretation": "High vegetation" if ndvi_value and ndvi_value > 0.5 else "Low vegetation"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching NDVI: {str(e)}")

# Test endpoint - fetch nightlight for a point
@router.post("/test/nightlight")
async def test_nightlight(request: NDVIRequest):
    """
    Test endpoint to fetch nightlight intensity for a single point.
    """
    from src.services.nightlight import nightlight_service
    
    try:
        nightlight_value = nightlight_service.get_nightlight_for_point(
            request.lat,
            request.lon
        )
        
        return {
            "lat": request.lat,
            "lon": request.lon,
            "nightlight": nightlight_value,
            "interpretation": "Dark area" if nightlight_value and nightlight_value < 10 else "Bright area"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching nightlight: {str(e)}")

# Main route generation endpoint
@router.post("/routes/generate", response_model=RouteResponse)
async def generate_route(request: RouteRequest):
    """
    Generate a dark and green walking route.
    
    - **distance**: Target distance in meters (e.g., 5000 for 5km)
    - **start_point**: Starting coordinates [longitude, latitude]
    - **start_location**: Optional district name (e.g., "Mitte")
    """
    # TODO: Implement actual route generation
    # For now, return a dummy response
    
    route_id = str(uuid.uuid4())
    
    # Dummy circular route around the start point
    start_lon, start_lat = request.start_point
    dummy_coordinates = [
        [start_lon, start_lat],
        [start_lon + 0.01, start_lat],
        [start_lon + 0.01, start_lat + 0.01],
        [start_lon, start_lat + 0.01],
        [start_lon, start_lat],
    ]
    
    return RouteResponse(
        route_id=route_id,
        coordinates=dummy_coordinates,
        distance=request.distance,
        darkness_score=0.75,  # Dummy score
        greenness_score=0.68,  # Dummy score
        estimated_time=int(request.distance / 80)  # ~80m per minute walking
    )

@router.get("/routes/{route_id}")
async def get_route(route_id: str):
    """
    Get details of a previously generated route.
    """
    # TODO: Implement route storage and retrieval
    raise HTTPException(
        status_code=404, 
        detail="Route not found. Route storage not yet implemented."
    )

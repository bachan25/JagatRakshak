from pydantic import BaseModel, Field
from typing import Optional

class LocationRequest(BaseModel):
    address: Optional[str] = Field(None, example="India Gate, New Delhi")
    latitude: Optional[float] = Field(None, example=19.0760)
    longitude: Optional[float] = Field(None, example=72.8777)

class LocationResponse(BaseModel):
    message: str = Field(..., example="Location retrieved successfully")
    city: str = Field(..., example="Berhampur")
    state: str = Field(..., example="Odisha")
    country: str = Field(..., example="India")
    address: Optional[str] = Field(None, example="near new bus stand, Berhampur")
    timestamp: str = Field(..., example="2025-08-16T01:40:09.526724")
    maps_url: str = Field(..., example="https://www.google.com/maps?q=19.3149,84.7941")

from fastapi import HTTPException,APIRouter
import httpx
import os
from dotenv import load_dotenv
from app.models.location import LocationRequest
import random
import datetime
load_dotenv()

router = APIRouter()
GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


@router.post("/get-location-details",summary="Get location details by address or GPS coordinates",status_code=200,response_description="Location details")
async def get_location_details(req: LocationRequest):
    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="Missing Google Maps API key")

    async with httpx.AsyncClient() as client:
        # Use address input
        if req.address:
            url = f"https://maps.googleapis.com/maps/api/geocode/json"
            params = {"address": req.address, "key": GOOGLE_API_KEY}
        # Use GPS coordinates
        elif req.latitude is not None and req.longitude is not None:
            url = f"https://maps.googleapis.com/maps/api/geocode/json"
            latlng = f"{req.latitude},{req.longitude}"
            params = {"latlng": latlng, "key": GOOGLE_API_KEY}
        else:
            raise HTTPException(status_code=400, detail="Provide address or latitude and longitude")

        response = await client.get(url, params=params)
        data = response.json()

        if data["status"] != "OK":
            raise HTTPException(status_code=404, detail="Location not found")

        return {
            "formatted_address": data["results"][0]["formatted_address"],
            "place_id": data["results"][0]["place_id"],
            "location": data["results"][0]["geometry"]["location"]
        }



# Simulated list of locations
locations = [
    {
        "city": "Bhubaneswar",
        "state": "Odisha",
        "country": "India",
        "address": "jaydev vihar overbridge",
        "latitude": 20.2961,
        "longitude": 85.8245
    },
    {
        "city": "Cuttack",
        "state": "Odisha",
        "country": "India",
        "address": "near high court square",
        "latitude": 20.4625,
        "longitude": 85.8828
    },
    {
        "city": "Berhampur",
        "state": "Odisha",
        "country": "India",
        "address": "near new bus stand, Berhampur",
        "latitude": 19.3149,
        "longitude": 84.7941
    }
]

@router.get("/current-location", summary="Get user current location", status_code=200, response_description="Current location details")
def get_current_location():
    # Pick a random location from the list
    location = random.choice(locations)
    
    # Create Google Maps shareable link
    maps_url = f"https://www.google.com/maps?q={location['latitude']},{location['longitude']}"
    
    return {
        "message": "User current location retrieved successfully",
        "city": location["city"],
        "state": location["state"],
        "country": location["country"],
        "address": location["address"],
        "timestamp": datetime.datetime.now().isoformat(),
        "maps_url": maps_url
    }

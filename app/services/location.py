import requests

def get_address_from_coords(lat: float, lon: float) -> str:
    try:
        response = requests.get(f"https://nominatim.openstreetmap.org/reverse",
                                params={"lat": lat, "lon": lon, "format": "json"})
        if response.status_code == 200:
            data = response.json()
            return data.get("display_name", "Unknown location")
    except Exception as e:
        print("Location error:", e)
    return "Unknown location"

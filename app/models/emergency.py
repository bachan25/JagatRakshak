from pydantic import BaseModel

class EmergencyReport(BaseModel):
    type: str
    latitude: float
    longitude: float
    user_contact: str

from pydantic import BaseModel
class VehicleInfoResponse(BaseModel):
    vehicle_number: str
    owner_name: str
    vehicle_type: str
    model: str
    registration_date: str
    rto_office: str
    contact_number: str
    address: str
from fastapi import APIRouter, HTTPException
import pandas as pd
from app.models.vehicle_info_model import VehicleInfoResponse

router = APIRouter()

# Sample RTO data in memory
data = [
    ["DL05AB1234", "Rajesh Kumar", "Car", "Maruti Swift", "2021-06-15", "Delhi RTO", "9876543210", "123 MG Road, Delhi"],
    ["MH12XY5678", "Priya Sharma", "Bike", "Honda Activa", "2020-09-20", "Pune RTO", "9123456780", "45 FC Road, Pune"],
    ["GJ01CD4321", "Amit Patel", "Car", "Hyundai i20", "2019-02-10", "Ahmedabad RTO", "9988776655", "78 Ring Road, Ahmedabad"],
    ["KA05MN8765", "Sneha Rao", "Scooter", "TVS Jupiter", "2022-01-05", "Bangalore RTO", "9090909090", "56 MG Road, Bangalore"],
    ["TN10PQ3456", "Arjun Reddy", "Car", "Tata Nexon", "2023-04-12", "Chennai RTO", "9012345678", "89 Mount Road, Chennai"]
]

columns = [
    "Vehicle Number", "Owner Name", "Vehicle Type", "Model", "Registration Date",
    "RTO Office", "Contact Number", "Address"
]

# Create DataFrame in memory
df = pd.DataFrame(data, columns=columns)

@router.get("/findvehicleinfo/{vehicle_number}",response_model=VehicleInfoResponse, summary="Get vehicle information by vehicle number")
def get_vehicle_info(vehicle_number: str):
    vehicle_number = vehicle_number.upper().strip()
    record = df[df["Vehicle Number"] == vehicle_number]

    if record.empty:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Convert DataFrame row to dict with snake_case keys
    result = {
        "vehicle_number": record.iloc[0]["Vehicle Number"],
        "owner_name": record.iloc[0]["Owner Name"],
        "vehicle_type": record.iloc[0]["Vehicle Type"],
        "model": record.iloc[0]["Model"],
        "registration_date": str(record.iloc[0]["Registration Date"]),
        "rto_office": record.iloc[0]["RTO Office"],
        "contact_number": record.iloc[0]["Contact Number"],
        "address": record.iloc[0]["Address"]
    }

    return VehicleInfoResponse(**result)

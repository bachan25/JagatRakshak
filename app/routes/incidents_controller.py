import base64
from fastapi import APIRouter, Depends, UploadFile, File,HTTPException
from requests import Session
from app.models.incidents import ImageURLListRequest,Incident, IncidentCreate, IncidentImage,IncidentResponse,IncidentImageCreate,IncidentImageResponse
from app.services.inidents_service import save_incident_image, find_incident_images,create_incident,get_incident,get_incidents_by_user,get_all_incidents,get_incidents_by_status,get_incidents_by_status_and_user,update_incident,get_incidents_by_state_and_country
from app.db.database import get_db
import requests

router = APIRouter()

@router.post("/create", response_model=IncidentResponse,summary="Report a new incident")
async def report_incident_controller(incident: IncidentCreate, db: Session = Depends(get_db)):
    try:
        response = create_incident(incident, db)
        return response
    except Exception as e:
        return {"message": "Error reporting incident", "error": str(e)}


# get incident by incident id
@router.get("/{incident_id}", response_model=IncidentResponse, summary="Get incident by ID")
async def get_incident_controller(incident_id: int, db: Session = Depends(get_db)):
    try:
        response = get_incident(incident_id, db)
        return response
    except Exception as e:
        return {"message": "Error fetching incident", "error": str(e)}

# get incident by user email
@router.get("/user/{user_email}", response_model=list[IncidentResponse], summary="Get incidents by user email")
async def get_incidents_by_user_controller(user_email: str, db: Session = Depends(get_db)):
    try:
        response = get_incidents_by_user(user_email, db)
        return response
    except Exception as e:
        return {"message": "Error fetching incidents", "error": str(e)}

# get all incidents
@router.get("/", response_model=list[IncidentResponse], summary="Get all incidents")
async def get_all_incidents_controller(db: Session = Depends(get_db)):
    try:
        response = get_all_incidents(db)
        return response
    except Exception as e:
        return {"message": "Error fetching incidents", "error": str(e)}
    
# filter by status
@router.get("/status/{status}", response_model=list[IncidentResponse], summary="Get all incidents by status")
async def get_incidents_by_status_controller(status: str, db: Session = Depends(get_db)):
    try:
        response = get_incidents_by_status(status, db)
        return response
    except Exception as e:
        return {"message": "Error fetching incidents", "error": str(e)}
    
# filter by status and email field
@router.get("/status/{status}/user/{user_email}", response_model=list[IncidentResponse], summary="Get all incidents by status and user email")
async def get_incidents_by_status_and_user_controller(status: str, user_email: str, db: Session = Depends(get_db)):
    try:
        response = get_incidents_by_status_and_user(status, user_email, db)
        return response
    except Exception as e:
        return {"message": "Error fetching incidents", "error": str(e)}

# update incident
@router.put("/update/{incident_id}", response_model=IncidentResponse, summary="Update incident")
async def update_incident_controller(incident_id: int, incident: IncidentCreate, db: Session = Depends(get_db)):
    try:
        response = update_incident(incident_id, incident, db)
        return response
    except Exception as e:
        return {"message": "Error updating incident", "error": str(e)}
# get all incidents by country and state
@router.get("/country/{country}/state/{state}", response_model=list[IncidentResponse], summary="Get all incidents by country and state")
async def get_incidents_by_country_and_state_controller(country: str, state: str, db: Session = Depends(get_db)):
    try:
        response = get_incidents_by_state_and_country(state,country,db)
        return response
    except Exception as e:
        return {"message": "Error fetching incidents", "error": str(e)}


@router.post("/{incident_id}/images")
async def upload_incident_images(
    incident_id: int,
    images: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        for img in images:
            # Read file and convert to Base64 string
            file_bytes = await img.read()
            file_base64 = base64.b64encode(file_bytes).decode("utf-8")
            save_incident_image(incident_id, file_base64, db)
        return {"message": "Images stored as Base64 successfully", "incident_id": incident_id}
    except Exception as e:
        return {"message": "Error uploading images", "error": str(e)}
    

# get incident images64
@router.get("/{incident_id}/images64", response_model=list[IncidentImageResponse], summary="Get incident images in base64 format")
async def get_incident_images(incident_id: int, db: Session = Depends(get_db)):
    try:
        images = find_incident_images(incident_id, db)
        return [IncidentImageResponse(id=img.id, incident_id=img.incident_id, file_data_base64=img.file_data_base64) for img in images]
    except Exception as e:
        return {"message": "Error fetching incident images", "error": str(e)}


# save incident images take input as IncidentImageCreate
@router.post("/images64", summary="Save incident image in base64 encoded format")
async def save_incident_image_base64(incidentImageCreate: IncidentImageCreate, db: Session = Depends(get_db)):
    try:
        for img in incidentImageCreate.images:
            save_incident_image(incidentImageCreate.incident_id, img, db)
        return {"message": "Images stored as Base64 successfully", "incident_id": incidentImageCreate.incident_id}
    except Exception as e:
        return {"message": "Error saving incident image", "error": str(e)}
    

# save incidents images received as url

@router.post("/upload-image-urls", summary="Upload incident images from URLs")
def upload_images_from_urls(data: ImageURLListRequest, db: Session = Depends(get_db)):
    # Check incident exists
    incident = db.query(Incident).filter(Incident.incident_id == data.incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    saved_images = []
    for url in data.image_urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Convert image content to base64
                image_base64 = base64.b64encode(response.content).decode("utf-8")
                save_incident_image(incident.incident_id, image_base64, db)
            else:
                saved_images.append({"url": url, "error": "Failed to fetch image"})
        except Exception as e:
            saved_images.append({"url": url, "error": str(e)})

    return "images saved successfully"

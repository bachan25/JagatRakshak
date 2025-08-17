from datetime import datetime
from sqlalchemy.orm import Session 
from sqlalchemy import func
from app.models.incidents import Incident, IncidentCreate,IncidentResponse,IncidentImage

def create_incident(incident: IncidentCreate, db: Session):
    db_incident = Incident(
        user_email=incident.user_email,
        incident_place=incident.incident_place,
        incident_type=incident.incident_type,
        victim_type=incident.victim_type,
        victim_details=incident.victim_details,
        incident_status=incident.incident_status,
        incident_state=incident.incident_state,
        incident_description=incident.incident_description,
        incident_country=incident.incident_country,
        incident_city=incident.incident_city,
        comment=incident.comment
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return IncidentResponse(
        incident_id=db_incident.incident_id,
        user_email=db_incident.user_email,
        created_date=db_incident.created_date,
        updated_date=db_incident.updated_date,
        incident_place=db_incident.incident_place,
        incident_type=db_incident.incident_type,
        victim_type=db_incident.victim_type,
        victim_details=db_incident.victim_details,
        incident_status=db_incident.incident_status,
        incident_state=db_incident.incident_state,
        incident_description=db_incident.incident_description,
        incident_country=db_incident.incident_country,
        incident_city=db_incident.incident_city,
        comment=db_incident.comment
    )



# get incident by id
def get_incident(incident_id: int, db: Session):
    return db.query(Incident).filter(Incident.incident_id == incident_id).first()


# get incidents by user email
def get_incidents_by_user(user_email: str, db: Session):
    return db.query(Incident).filter(Incident.user_email == user_email).all()


# get all incidents
def get_all_incidents(db: Session):
    return db.query(Incident).all()


# get incidents by status
def get_incidents_by_status(status: str, db: Session):
    return db.query(Incident).filter(Incident.incident_status == status).all()


# get incidents by status and user email
def get_incidents_by_status_and_user(status: str, user_email: str, db: Session):
    return db.query(Incident).filter(Incident.incident_status == status, Incident.user_email == user_email).all()


# update_incident
def update_incident(incident_id: int, incident: IncidentCreate, db: Session):
    db_incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not db_incident:
        return {"message": "Incident not found"}
    db_incident.user_email = incident.user_email
    db_incident.incident_place = incident.incident_place
    db_incident.incident_type = incident.incident_type
    db_incident.victim_type = incident.victim_type
    db_incident.victim_details = incident.victim_details
    db_incident.incident_status = incident.incident_status
    db_incident.incident_state = incident.incident_state
    db_incident.incident_description = incident.incident_description
    db_incident.incident_country = incident.incident_country
    db_incident.incident_city = incident.incident_city
    db_incident.updated_date = datetime.now()
    db_incident.comment = incident.comment
    db.commit()
    db.refresh(db_incident)
    return IncidentResponse(
        incident_id=db_incident.incident_id,
        user_email=db_incident.user_email,
        created_date=db_incident.created_date,
        updated_date=db_incident.updated_date,
        incident_place=db_incident.incident_place,
        incident_type=db_incident.incident_type,
        victim_type=db_incident.victim_type,
        victim_details=db_incident.victim_details,
        incident_status=db_incident.incident_status,
        incident_description=db_incident.incident_description,
        incident_state=db_incident.incident_state,
        incident_city=db_incident.incident_city,
        incident_country=db_incident.incident_country,
        comment=db_incident.comment
    )

# get_incidents_by_state and country
def get_incidents_by_state_and_country(state: str, country: str, db: Session):
    return db.query(Incident).filter(
    func.lower(Incident.incident_state) == state.lower(),
    func.lower(Incident.incident_country) == country.lower()
).all()

# save_incident_image
def save_incident_image(incident_id: int, file_data_base64: str, db: Session):
    db_image = IncidentImage(
        incident_id=incident_id,
        file_data_base64=file_data_base64
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

# find_incident_images
def find_incident_images(incident_id: int, db: Session):
    images = db.query(IncidentImage).filter(IncidentImage.incident_id == incident_id).all()
    return images
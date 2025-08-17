from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from app.db.database import Base
from pydantic import BaseModel,Field
from sqlalchemy.orm import relationship

class Incident(Base):
    __tablename__ = "incidents"

    incident_id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    updated_date = Column(DateTime, default=datetime.now)
    incident_place = Column(String, nullable=False)
    incident_state = Column(String, nullable=False)  # e.g., "odisha", "maharashtra"
    incident_country = Column(String, nullable=False)  # e.g., "india", "usa"
    incident_city = Column(String, nullable=False)  # e.g., "bhubaneswar", "mumbai"
    incident_description = Column(Text, nullable=True)  # Description of the incident
    incident_type = Column(String, nullable=False)  # road accident, fire tragedy, etc.
    victim_type = Column(String, nullable=False)    # self, others
    victim_details = Column(Text, nullable=True)    # name, address, contact details
    incident_status = Column(String, default="inprogress")  # inprogress, pending, resolved
    comment = Column(Text, nullable=True)

class IncidentImage(Base):
    __tablename__ = "incident_images"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, nullable=False)
    file_data_base64 = Column(Text, nullable=False)  # Base64 string of the image

class IncidentImageCreate(BaseModel):
    images: list[str] = Field(..., example=["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA..."])
    incident_id: int = Field(..., example=1)
class ImageURLListRequest(BaseModel):
    incident_id: int = Field(..., example=1)
    image_urls: List[str] = Field(..., example=["http://example.com/image1.png", "http://example.com/image2.png"])

class IncidentImageResponse(BaseModel):
    id: int
    incident_id: int
    file_data_base64: str

class IncidentCreate(BaseModel):
    user_email: str = Field(..., example="alice@example.com")
    incident_place: str = Field(..., example="Main Street")
    incident_state: str = Field(..., example="odisha")  # e.g., "odisha", "maharashtra"
    incident_country: str = Field(..., example="india")  # e.g., "india", "usa"
    incident_city: str = Field(..., example="bhubaneswar")  # e.g., "bhubaneswar", "mumbai"
    incident_type: str = Field(..., example="road accident")
    victim_type: str = Field(..., example="self")
    incident_description: Optional[str] = Field(None, example="Description of the incident")
    victim_details: Optional[str] = Field(None, example="John Doe, 123 Main St, 555-1234")
    incident_status: Optional[str] = Field("inprogress", example="inprogress")
    comment: Optional[str] = None


class IncidentResponse(BaseModel):
    incident_id: int
    user_email: str
    created_date: datetime
    updated_date: datetime
    incident_place: str
    incident_state: str
    incident_country: str
    incident_city: str
    incident_type: str
    incident_description: Optional[str]
    victim_type: str
    victim_details: Optional[str]
    incident_status: str
    comment: Optional[str]




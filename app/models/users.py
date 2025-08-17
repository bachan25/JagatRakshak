from pydantic import BaseModel, Field,constr
from app.db.database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    city = Column(String, index=True)
    phone = Column(String, index=True)
    password = Column(String, index=True)
    country = Column(String, index=True)
    state = Column(String, index=True)
    address = Column(String, index=True)
    pin = Column(String, index=True)
    user_type = Column(String, index=True)
    service_type = Column(String, index=True)


# Request body schema
class UserCreateRequest(BaseModel):
    name: str = Field(..., example="Alice")
    email: str = Field(..., example="alice@example.com")
    city: str = Field(..., example="Mumbai")
    phone: str = Field(..., example="9876543210")
    password: str = Field(..., min_length=6, example="securepassword")
    country: str = Field(..., example="India")
    state: str = Field(..., example="Maharashtra")
    city: str = Field(..., example="Mumbai")
    address: str = Field(..., example="123 Main St")
    pin: str = Field(..., example="400001")
    user_type: str = Field(..., example="individual,organization")
    service_type: str = Field(..., example="hospital,volunteer,police station etc")

# Response schema
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    city: str
    phone: str
    country: str
    state: str
    address: str
    pin: str
    user_type: str
    service_type: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_type: str
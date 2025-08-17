from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.users import User
from app.models.users import UserCreateRequest, UserResponse


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or user.password != password:
        return None
    return user

def create_user(db: Session, user: UserCreateRequest):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    db_user = User(name=user.name, email=user.email, password=user.password, city=user.city, phone=user.phone, country=user.country, state=user.state, address=user.address, pin=user.pin, user_type=user.user_type, service_type=user.service_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse(
    id=db_user.id,
    name=db_user.name,
    email=db_user.email,
    city=db_user.city,
    phone=db_user.phone,
    country=db_user.country,
    state=db_user.state,
    address=db_user.address,
    pin=db_user.pin,
    user_type=db_user.user_type,
    service_type=db_user.service_type
)

# get_user_by_id
def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        city=user.city,
        phone=user.phone,
        country=user.country,
        state=user.state,
        address=user.address,
        pin=user.pin,
        user_type=user.user_type,
        service_type=user.service_type
    )

def get_users(db: Session):
    users = db.query(User).all()
    return [UserResponse(id=user.id, name=user.name, email=user.email, city=user.city, phone=user.phone, country=user.country, state=user.state, address=user.address, pin=user.pin, user_type=user.user_type, service_type=user.service_type) for user in users]
def get_user(db: Session, email_id: str):
    user = db.query(User).filter(User.email == email_id).first()
    if not user:
        return None
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        city=user.city,
        phone=user.phone,
        country=user.country,
        state=user.state,
        address=user.address,
        pin=user.pin,
        user_type=user.user_type,
        service_type=user.service_type
    )

def delete_user(db: Session, email_id: str):
    user = db.query(User).filter(User.email == email_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()



# search_volunteer_users_by_state_country_city
def search_volunteer_users_by_state_country_city(db: Session, state: str, country: str, city: str):
    query = db.query(User).filter(func.lower(User.user_type) != "individual")
    if state:
        query = query.filter(func.lower(User.state) == state.lower())
    if country:
        query = query.filter(func.lower(User.country) == country.lower())
    if city:
        query = query.filter(func.lower(User.city) == city.lower())
    users = query.all()
    return [UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        city=user.city,
        phone=user.phone,
        country=user.country,
        state=user.state,
        address=user.address,
        pin=user.pin,
        user_type=user.user_type,
        service_type=user.service_type
    ) for user in users]
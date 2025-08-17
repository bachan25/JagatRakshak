from fastapi import APIRouter, Depends, HTTPException
from app import db
from app.models.users import UserCreateRequest, UserResponse,UserLoginRequest,UserLoginResponse
from app.services.user_service import create_user ,get_user_by_id, get_users,get_user,authenticate_user,delete_user, search_volunteer_users_by_state_country_city
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.utils.jwt_handler import create_access_token,verify_token


router = APIRouter()


@router.get("/", response_model=list[UserResponse], summary="Get all users")
async def get_users_controller(db: Session = Depends(get_db)):
    users = get_users(db)
    return users

@router.post("/add", response_model=UserResponse, status_code=201, summary="Create a new user")
async def create_user_controller(user: UserCreateRequest,db: Session = Depends(get_db)):
    try:
        created_user = create_user(db,user)
        return created_user
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise e

@router.get("/{email_id}", response_model=UserResponse, summary="Get a user by email ID")
async def get_user_controller(email_id: str, db: Session = Depends(get_db)):
    user = get_user(db, email_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# get user by user id
@router.get("/by_id/{user_id}", response_model=UserResponse, summary="Get a user by ID")
async def get_user_by_id_controller(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/login", response_model=UserLoginResponse, summary="User login by email id and password")
async def login_user_controller(userLoginRequest: UserLoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, userLoginRequest.email, userLoginRequest.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": userLoginRequest.email})
    return UserLoginResponse(
        access_token=token,
        user_type=user.user_type,
        token_type="bearer"
    )
@router.post("/logout", summary="User logout")
async def logout_user_controller(db: Session = Depends(get_db)):
    # Invalidate the user's token (implementation depends on your auth strategy)

    return {"msg": "User logged out successfully"}
# verify token
@router.get("/verify/token", summary="Verify access token")
async def verify_token_controller(token: str):
    print("token:", token)
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"msg": "Token is valid", "user": payload}

@router.get("/by_token",response_model=UserResponse, summary="Get user by token")
async def get_user_by_token_controller(token: str):
    print( "token:", token)
    payload = verify_token(token)
    print("payload:", payload)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    email = payload.get("sub")
    print(email)
    user = get_user(db, email)
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# delete user by emailid
@router.delete("/{email_id}", summary="Delete a user by email ID")
async def delete_user_controller(email_id: str, db: Session = Depends(get_db)):
    try:
        delete_user(db, email_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")

    return {"msg": "User deleted successfully"}


# search volunteer user by country, state and city
@router.get("/search/volunteers", response_model=list[UserResponse], summary="Search volunteer users by country, state and city")
async def search_volunteer_users_controller(country: str = None, state: str = None, city: str = None, db: Session = Depends(get_db)):
    return search_volunteer_users_by_state_country_city(db, state, country, city)
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_admin_user
from app.crud import user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate

router = APIRouter()

@router.post("/", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
):
    existing_user = user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    existing_user = user.get_by_username(db, username=user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    created_user = user.create(db, obj_in=user_in)
    return created_user

@router.get("/", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
):
    users = user.get_multi(db, skip=skip, limit=limit)
    return users

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
):
    return current_user

@router.get("/{user_id}", response_model=UserSchema)
def read_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_user = user.get(db, id=user_id)
    if db_user == current_user:
        return db_user
    if not user.is_admin(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return db_user

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
):
    db_user = user.get(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user != current_user and not user.is_admin(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    updated_user = user.update(db, db_obj=db_user, obj_in=user_in)
    return updated_user
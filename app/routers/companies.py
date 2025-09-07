from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_admin_user
from app.crud import company
from app.models.user import User
from app.schemas.company import Company, CompanyCreate, CompanyUpdate

router = APIRouter()

@router.post("/", response_model=Company)
def create_company(
    *,
    db: Session = Depends(get_db),
    company_in: CompanyCreate,
    current_user: User = Depends(get_current_admin_user),
):
    created_company = company.create(db, obj_in=company_in)
    return created_company

@router.get("/", response_model=List[Company])
def read_companies(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
):
    companies = company.get_multi(db, skip=skip, limit=limit)
    return companies

@router.get("/{company_id}", response_model=Company)
def read_company(
    *,
    db: Session = Depends(get_db),
    company_id: int,
    current_user: User = Depends(get_current_active_user),
):
    db_company = company.get(db, id=company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@router.put("/{company_id}", response_model=Company)
def update_company(
    *,
    db: Session = Depends(get_db),
    company_id: int,
    company_in: CompanyUpdate,
    current_user: User = Depends(get_current_admin_user),
):
    db_company = company.get(db, id=company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    updated_company = company.update(db, db_obj=db_company, obj_in=company_in)
    return updated_company

@router.delete("/{company_id}")
def delete_company(
    *,
    db: Session = Depends(get_db),
    company_id: int,
    current_user: User = Depends(get_current_admin_user),
):
    db_company = company.get(db, id=company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    company.remove(db, id=company_id)
    return {"message": "Company deleted successfully"}
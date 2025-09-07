from pydantic import BaseModel
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    mode: Optional[str] = None
    rating: Optional[float] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    mode: Optional[str] = None
    rating: Optional[float] = None

class Company(CompanyBase):
    id: int

    class Config:
        from_attributes = True
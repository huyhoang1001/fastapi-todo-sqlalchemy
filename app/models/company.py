from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    mode = Column(String)
    rating = Column(Float)
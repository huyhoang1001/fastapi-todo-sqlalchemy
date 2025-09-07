from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    summary = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="pending")
    priority = Column(String, default="medium")
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="tasks")
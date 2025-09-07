from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def create_with_owner(self, db: Session, *, obj_in: TaskCreate, owner_id: int) -> Task:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, user_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        return (
            db.query(self.model)
            .filter(Task.user_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

task = CRUDTask(Task)
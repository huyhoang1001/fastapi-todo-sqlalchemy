from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.crud import task
from app.models.user import User
from app.schemas.task import Task, TaskCreate, TaskUpdate

router = APIRouter()

@router.post("/", response_model=Task)
def create_task(
    *,
    db: Session = Depends(get_db),
    task_in: TaskCreate,
    current_user: User = Depends(get_current_active_user),
):
    created_task = task.create_with_owner(db, obj_in=task_in, owner_id=current_user.id)
    return created_task

@router.get("/", response_model=List[Task])
def read_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
):
    tasks = task.get_multi_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return tasks

@router.get("/{task_id}", response_model=Task)
def read_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_active_user),
):
    db_task = task.get(db, id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return db_task

@router.put("/{task_id}", response_model=Task)
def update_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    task_in: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
):
    db_task = task.get(db, id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    updated_task = task.update(db, db_obj=db_task, obj_in=task_in)
    return updated_task

@router.delete("/{task_id}")
def delete_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_active_user),
):
    db_task = task.get(db, id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    task.remove(db, id=task_id)
    return {"message": "Task deleted successfully"}
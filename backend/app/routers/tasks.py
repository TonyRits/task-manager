from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app import models, schemas
from app.database import get_db
from app.utils import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=schemas.TaskResponse, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_task = models.Task(**task.model_dump(), owner_id=user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/")
def get_tasks(
    completed: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(models.Task).filter(models.Task.owner_id == user.id)
    
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    
    total = query.count()
    tasks = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "tasks": tasks
    }


@router.get("/{id}", response_model=schemas.TaskResponse)
def get_task(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.query(models.Task).filter(
        models.Task.id == id,
        models.Task.owner_id == user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{id}", response_model=schemas.TaskResponse)
def update_task(id: int, update: schemas.TaskUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.query(models.Task).filter(
        models.Task.id == id,
        models.Task.owner_id == user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{id}", status_code=204)
def delete_task(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.query(models.Task).filter(
        models.Task.id == id,
        models.Task.owner_id == user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
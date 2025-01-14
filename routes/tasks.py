from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from auth.jwt import get_current_user
from models.task import Task as TaskSchema, TaskCreate
from database.database import SessionLocal, get_db, Task as TaskModel

router = APIRouter()

@router.post("/", response_model=TaskSchema)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_task = TaskModel(
        titulo=task.titulo,
        descricao=task.descricao,
        estado=task.estado,
        data_criacao=datetime.utcnow(),
        data_atualizacao=datetime.utcnow()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[TaskSchema])
def list_tasks(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return db.query(TaskModel).all()

@router.get("/{task_id}", response_model=TaskSchema)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{task_id}", response_model=TaskSchema)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.titulo = task.titulo
    db_task.descricao = task.descricao
    db_task.estado = task.estado
    db_task.data_atualizacao = datetime.utcnow()
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}
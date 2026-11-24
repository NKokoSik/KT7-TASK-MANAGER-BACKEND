from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.tasks import create_task, update_task
from app.tasks.notifications import notify_task_created

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])

def owned_project(db: Session, project_id: int, user_id: int):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == user_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def add_task(project_id: int, data: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = owned_project(db, project_id, user.id)
    try:
        task = create_task(db, data, project, user.id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    notify_task_created.delay(user.id, task.title)
    return task

@router.get("", response_model=list[TaskRead])
def list_tasks(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = owned_project(db, project_id, user.id)
    return db.query(Task).filter(Task.project_id == project.id).order_by(Task.id.desc()).all()

@router.patch("/{task_id}", response_model=TaskRead)
def edit_task(project_id: int, task_id: int, data: TaskUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = owned_project(db, project_id, user.id)
    task = db.query(Task).filter(Task.id == task_id, Task.project_id == project.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    try:
        return update_task(db, task, data)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(project_id: int, task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = owned_project(db, project_id, user.id)
    task = db.query(Task).filter(Task.id == task_id, Task.project_id == project.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()

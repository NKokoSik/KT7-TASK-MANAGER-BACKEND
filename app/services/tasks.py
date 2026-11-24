from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.project import Project
from app.schemas.task import TaskCreate, TaskUpdate

VALID_STATUSES = {"todo", "in_progress", "done"}

def create_task(db: Session, data: TaskCreate, project: Project, creator_id: int) -> Task:
    if data.status not in VALID_STATUSES:
        raise ValueError("Invalid task status")
    task = Task(**data.model_dump(), project_id=project.id, creator_id=creator_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, task: Task, data: TaskUpdate) -> Task:
    values = data.model_dump(exclude_unset=True)
    if "status" in values and values["status"] not in VALID_STATUSES:
        raise ValueError("Invalid task status")
    for key, value in values.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

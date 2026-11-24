from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.notification import Notification

@celery_app.task(name="notifications.task_created")
def notify_task_created(user_id: int, task_title: str):
    db = SessionLocal()
    try:
        notification = Notification(user_id=user_id, message=f'Задача «{task_title}» создана')
        db.add(notification)
        db.commit()
        return {"notification_id": notification.id, "user_id": user_id}
    finally:
        db.close()

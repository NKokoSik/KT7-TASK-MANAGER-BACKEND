from pydantic import BaseModel, ConfigDict

class NotificationRead(BaseModel):
    id: int
    message: str
    is_read: bool
    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, Field, ConfigDict

class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    description: str | None = None
    status: str = "todo"

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=160)
    description: str | None = None
    status: str | None = None

class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    project_id: int
    creator_id: int
    model_config = ConfigDict(from_attributes=True)

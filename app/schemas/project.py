from pydantic import BaseModel, Field, ConfigDict

class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str | None = None

class ProjectRead(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

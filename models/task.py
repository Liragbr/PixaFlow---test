from pydantic import BaseModel, Field
from datetime import datetime

class TaskBase(BaseModel):
    titulo: str = Field(..., min_length=1)
    descricao: str = None
    estado: str = Field(..., pattern="^(pendente|em andamento|concluída)$")

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        orm_mode = True

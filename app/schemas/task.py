from pydantic import BaseModel,Field
from typing import Optional


class TaskCreate(BaseModel):
    title : str
    priority : int


class TaskRead(BaseModel):
    id : int
    title : str
    priority : int
    status : str
    project_id : int
    assigned_to : int|None


    class config():
        orm_mode = True


   
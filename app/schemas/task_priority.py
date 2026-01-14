from pydantic import BaseModel

class TaskPriorityUpdate(BaseModel):
    priority : int
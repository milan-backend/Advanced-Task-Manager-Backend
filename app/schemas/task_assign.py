from pydantic import BaseModel
from typing import Optional 


class TaskAssign(BaseModel):
    assigned_to : Optional[int]
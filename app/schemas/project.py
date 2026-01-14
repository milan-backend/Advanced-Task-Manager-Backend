from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name : str


class ProjectRead(BaseModel):
    id : int
    name : str
    owner_id : int




    class config():
       orm_mode = True

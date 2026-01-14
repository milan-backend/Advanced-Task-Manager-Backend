from pydantic import BaseModel


class ProjectMemberCreate(BaseModel):
    user_id : int


class ProjectMemberRead(BaseModel):
    id : int
    project_id :int
    user_id : int
    role : str


    class config():
       orm_mode = True
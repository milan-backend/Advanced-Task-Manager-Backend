from fastapi import FastAPI

from app.api.users import router as user_router
from app.api.projects import router as project_router
from app.api.project_members import router as project_member_router
from app.api.tasks import router as task_router
from app.api.auth import router as auth_router


app = FastAPI()

app.include_router(user_router)
app.include_router(project_router)
app.include_router(project_member_router)
app.include_router(task_router)
app.include_router(auth_router)
from fastapi import APIRouter,Depends,HTTPException,status,Query
from sqlalchemy.orm import Session
from typing import List

from app.models.project import Project
from app.api.deps import get_db
from app.schemas.project import ProjectCreate,ProjectRead
from app.services.project_service import create_project
from app.auth.deps import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post("/projects",response_model=ProjectRead)
def create_project_endpoint(
    project_in : ProjectCreate,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):

    project = create_project(
        db=db, 
        project_in=project_in, 
        owner_id=current_user.id)

    return project



@router.get("/projects",response_model=List[ProjectRead])
def read_projects(
                  limit : int = Query(10,ge=0,le=100),
                  offset : int = Query(0,ge=0),
                  db : Session = Depends(get_db),
                  current_user : User = Depends(get_current_user)):


    projects = db.query(Project).filter(Project.owner_id == current_user.id).offset(offset).limit(limit).all()

    return projects



@router.get("/projects/{project_id}",response_model=ProjectRead)
def read_project(
    project_id : int,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    
    
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Project not found."
        )
    
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorised to access this project."
        )
    
    return project
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.schemas.project_member import ProjectMemberCreate,ProjectMemberRead
from app.services.project_member_service import add_project_member
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.auth.deps import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/projects/{project_id}/members",
    tags=["project-members"],
)


@router.post("",
             response_model=ProjectMemberRead)
def add_member_endpoint(
    project_id : int,
    member_in : ProjectMemberCreate,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    
    

    member = add_project_member(
        db=db,
        member_in=member_in,
        project_id=project_id,
        current_user_id= current_user.id,
    )

    return member



@router.get("", 
            response_model= List[ProjectMemberRead])
def list_project_members(
    project_id : int,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    


    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Project not found."
        )
    
    is_owner = project.owner_id == current_user.id

    is_member = (
        db.query(ProjectMember)
        .filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id,
    ).first()
     is not None
    )


    if not is_owner and not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = "Not authorized to see project member."
        )
    
    members = db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()


    return members
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException,status

from app.models.project_member import ProjectMember
from app.models.user import User
from app.models.project import Project
from app.schemas.project_member import ProjectMemberCreate


def add_project_member(
        project_id : int,
        member_in : ProjectMemberCreate,
        db : Session,
        current_user_id : int
) -> ProjectMember:
    
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Project not found."
        )
    
    if project.owner_id != current_user_id:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail= "Only project owner can add member."
        )
    
    user = db.query(User).filter(User.id == member_in.user_id).first()

    if not user:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        ) 
    
    member = ProjectMember(
        user_id = member_in.user_id,
        project_id = project_id,
        role = "member"
    )

    db.add(member)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail = "User is already a member of this project"
        )
    
    db.refresh(member)
    
    return member




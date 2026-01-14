from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from sqlalchemy.exc import IntegrityError

from app.schemas.task import TaskCreate
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.task import Task



def create_task(
        db : Session,
        project_id : int,
        task_in : TaskCreate,
        current_user_id : int,
) -> Task:
    
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Project not found."
        )

    is_owner = project.owner_id == current_user_id

    is_member = (db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user_id,
    ).first()
        is not None
    )


    if not is_owner and not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail = "Not aurthorized to create task in this project."
        )
    
        
    task = Task(
        title = task_in.title,
        project_id = project_id,
        status ="todo",
        priority = task_in.priority
        
    )

    db.add(task)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "Bad data request"
        )
    
    db.refresh(task)
    
    return task


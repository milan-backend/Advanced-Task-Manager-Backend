from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from app.schemas.task_status import TaskStatusUpdate
from app.models.task import Task
from app.models.project import Project
from app.models.project_member import ProjectMember
from sqlalchemy.exc import IntegrityError


def update_task_status(
        db : Session,
        task_id : int,
        status_in : TaskStatusUpdate,
        current_user_id : int
) -> Task:
    
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Task not found."
        )
    
    project = db.query(Project).filter(Project.id ==task.project_id).first()

    is_owner = project.owner_id == current_user_id

    is_member = (db.query(ProjectMember)
                 .filter(
                     ProjectMember.project_id == project.id,
                     ProjectMember.user_id == current_user_id
                 ).first()
                 is not None
)
    
    if not is_owner and not is_member:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail = "Not authorized to update status for this task."
        )
    

    task.status = status_in.status

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "Invalid task status."
        )
    db.refresh(task)

    return task
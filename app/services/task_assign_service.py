from sqlalchemy.orm import Session
from app.schemas.task_assign import TaskAssign
from app.models.task import Task
from fastapi import HTTPException,status
from app.models.project import Project
from app.models.project_member import ProjectMember




def assign_task(
        db:Session,
        task_id : int,
        assign_in : TaskAssign,
        current_user_id : int,
) -> Task:
    
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Task not found."
        )
    
    project = db.query(Project).filter(Project.id == task.project_id).first()

    is_owner = project.owner_id == current_user_id

    is_member = (db.query(ProjectMember)
                 .filter(
                     ProjectMember.project_id == project.id,
                    ProjectMember.user_id == current_user_id,
                 ).first()
                 is not None
                 )
    
    if not is_owner and not is_member:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail = "Not authorized to assign this task."
        )
    

    if assign_in.assigned_to is None:
        assign_in.assigned_to = None
        db.commit()
        db.refresh(task)
        return task
    

    assignee = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project.id,
                ProjectMember.user_id == assign_in.assigned_to)
    .first()
    )

    if not assignee:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Assigned user is not a member of this project."
        )
    
    task.assigned_to = assign_in.assigned_to
    db.commit()
    db.refresh(task)

    return task
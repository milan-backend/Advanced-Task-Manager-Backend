from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from app.models.task import Task
from app.models.project import Project


def task_delete(
        task_id : int,
        db : Session,
        current_user_id : int
) -> None:
    
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "task not found."
        )
    
    
    project = db.query(Project).filter(Project.id == task.project_id).first()

    if project.owner_id != current_user_id :
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail = "Only project owner can delete this task."
        )
    
    db.delete(task)
    db.commit()


    





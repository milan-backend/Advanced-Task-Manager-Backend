from fastapi import APIRouter,Depends,HTTPException,status,Response,Query
from sqlalchemy.orm import Session
from app.api.deps import get_db

from app.schemas.task import TaskCreate,TaskRead
from app.services.task_service import create_task
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.task import Task
from app.schemas.task_assign import TaskAssign
from app.services.task_assign_service import assign_task
from app.schemas.task_status import TaskStatusUpdate
from app.services.task_status_service import update_task_status
from app.schemas.task_priority import TaskPriorityUpdate
from app.services.task_priority_service import update_task_priority
from app.services.task_delete_service import task_delete
from app.auth.deps import get_current_user
from app.models.user import User
from typing import Optional


router = APIRouter(
    prefix="/projects/{project_id}/tasks",
    tags= ["tasks"],
)


@router.post("",
             response_model=TaskRead)
def create_task_endpoint(
    project_id : int,
    task_in : TaskCreate,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    
    task = create_task(
        db = db,
        project_id = project_id,
        task_in = task_in,
        current_user_id = current_user.id
    )

    return task




@router.get("",
            response_model=list[TaskRead])
def list_task(
    project_id : int,
    status : Optional[str] = Query(None),
    priority : Optional[int] = Query(None,ge=1,le=5), 
    limit : int = Query(10,ge=1,le=100),
    offset : int = Query(0,ge=0),
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user),
):

    project = (db.query(Project)
               .filter(Project.id == project_id)
               .first()
)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Project not found."
        )
    
    is_owner = project.owner_id == current_user.id

    is_member = (db.query(ProjectMember)
                 .filter(
                     ProjectMember.project_id == project_id,
                     ProjectMember.user_id == current_user.id
                 ).first()
                 is not None
                 )
    
    if not is_owner and not is_member:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail = "Not authorized to view task in this project."
        )
    

    query = db.query(Task).filter(Task.project_id == project_id)

    if status is not None:
        query = query.filter(Task.status == status)

    if priority is not None:
        query = query.filter(Task.priority == priority)

    tasks = (
        query.offset(offset).limit(limit).all()
    )
    return tasks



@router.patch("/tasks/{task_id}/assign",response_model=TaskRead)
def task_assign_endpoint(
    task_id : int,
    assign_in : TaskAssign,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):

    task = assign_task(
        db = db,
        assign_in = assign_in,
        task_id = task_id,
        current_user_id=current_user.id
    )

    return task




@router.patch("/{task_id}/status",response_model=TaskRead)
def task_status_endpoint(
    task_id : int,
    status_in : TaskStatusUpdate,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)

):
    


    task = update_task_status(
        db = db,
        task_id = task_id,
        status_in = status_in,
        current_user_id = current_user.id
    )

    return task




@router.patch("/{task_id}/priority",response_model=TaskRead)
def task_priority_endpoint(
    task_id : int,
    priority_in : TaskPriorityUpdate,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    
    
    task = update_task_priority(
        db = db,
        task_id = task_id,
        priority_in=priority_in,
        current_user_id=current_user.id
    )

    
    return task




@router.delete("/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(
    task_id : int,
    db : Session = Depends(get_db),
    current_user :User = Depends(get_current_user)
):

    task = task_delete(
        db = db,
        task_id = task_id,
        current_user_id=current_user.id
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


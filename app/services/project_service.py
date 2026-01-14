from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate


def create_project(
        db : Session,
        project_in : ProjectCreate,
        owner_id : int
) -> Project:
    
    project = Project(
        name = project_in.name,
        owner_id = owner_id
   )
    
    db.add(project)
    db.commit()
    db.refresh(project)

    return project
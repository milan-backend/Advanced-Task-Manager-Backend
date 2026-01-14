from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from app.db.base import Base

class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    project_id = Column(Integer,ForeignKey("projects.id"),nullable=False)
    role = Column(String, nullable = False)

    __table_args__ = (
       UniqueConstraint
                     ("user_id","project_id", name = "unique_user_project"),
    )
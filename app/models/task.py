from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)

    status = Column(String, nullable=False, default="todo")
    priority = Column(Integer, nullable=False)


    __table_args__ = (
        CheckConstraint
        ("status IN ('todo', 'in_progress', 'done')",
                        name = "task_status_check"
                        ),

        CheckConstraint(
            "priority >= 1 AND priority <= 5",
            name = "task_priority_check"
        ),
    )





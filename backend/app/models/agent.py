from datetime import datetime

from app.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    goal = Column(String, nullable=False)
    status = Column(String, default="in_progress")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tasks = relationship(
        "Task",
        back_populates="goal",
        cascade="all, delete-orphan",
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, default="pending")

    goal = relationship("Goal", back_populates="tasks")

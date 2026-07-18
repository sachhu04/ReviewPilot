from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from core.database import Base

class Statistics(Base):
    """
    A snapshot of statistics for the dashboard.
    Updated periodically or via triggers to avoid heavy aggregation on every load.
    """
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    total_reviews = Column(Integer, default=0)
    average_score = Column(Float, default=0.0)
    critical_issues_found = Column(Integer, default=0)
    merge_ready_percentage = Column(Float, default=0.0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

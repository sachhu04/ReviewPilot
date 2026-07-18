from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False)
    severity = Column(String, nullable=False)  # Critical, High, Medium, Low
    category = Column(String, nullable=False)  # Security, Performance, Logic, etc.
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    evidence = Column(String, nullable=True)
    recommendation = Column(String, nullable=True)
    confidence = Column(Integer, nullable=True)
    file_path = Column(String, nullable=True)
    line_number = Column(Integer, nullable=True)

    review = relationship("Review", back_populates="issues")

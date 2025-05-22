from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 🧱 SQLAlchemy Model
class RecordModel(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

# 🧾 Pydantic Schema
class Record(BaseModel):
    id: int = Field(..., description="Unique identifier of the record")
    name: str = Field(..., description="Name associated with the record")
    value: float = Field(..., description="Measured or calculated value")
    timestamp: datetime = Field(..., description="Timestamp of the record")

    class Config:
        orm_mode = True

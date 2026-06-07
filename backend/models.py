
from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.database import Base

class SleepRecord(Base):
    __tablename__ = "sleep_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    quality = Column(String, nullable=True)
    source = Column(String, nullable=True)


class WorkoutRecord(Base):
    __tablename__ = "workout_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    calories_burned = Column(Float, nullable=True)
    source = Column(String, nullable=True)
    activity_type = Column(String, nullable=True)   # "strength", "running"
    distance_meters = Column(Float, nullable=True)
    avg_heart_rate = Column(Integer, nullable=True)
    max_heart_rate = Column(Integer, nullable=True)

class HeartRateRecord(Base):
    __tablename__ = "heart_rate_metrics"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    time = Column(DateTime, nullable=False)
    bpm = Column(Float, nullable=False)
    source = Column(String, nullable=True)
    metric_type = Column(String, nullable=False)

class BodyMetricsRecord(Base):
    __tablename__ = "body_metrics"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    time = Column(DateTime, nullable=False)
    metric_type = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    source = Column(String, nullable=True)
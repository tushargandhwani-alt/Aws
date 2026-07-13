from database import Base
from sqlalchemy import Column, Integer, String , CheckConstraint

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False)
    age = Column(Integer, CheckConstraint("age > 0"), nullable=False)
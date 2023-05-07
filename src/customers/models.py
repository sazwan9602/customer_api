from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from src.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String(100), unique=True, index=True)
    address = Column(String(250))
    phone_no = Column(String(12))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

from pydantic import BaseModel, EmailStr, validator
from fastapi import HTTPException
from datetime import datetime
import re


class Customer(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    address: str
    phone_no: str
    created_at: datetime

    class Config:
        orm_mode = True

    @validator('phone_no')  # validate malaysia phone number
    def validate_phone_number(cls, v):
        pattern = r"^(?:\+?6?01)[0-46-9]-*[0-9]{7,8}$"
        if not re.match(pattern, v):
            raise HTTPException(status_code=400, detail="Invalid phone number format")
        return v

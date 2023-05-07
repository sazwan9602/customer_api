from .models import Customer
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def checkExistingEmail(db: Session, email):  # validate unique value
    cust_email = db.query(Customer).filter(Customer.email == email).first()
    if cust_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Email "{email}" already exist.')

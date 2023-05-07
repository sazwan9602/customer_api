from .schema import Customer as CustomerSchema
from .models import Customer
from . import service
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def get(db: Session, cid: int):
    db_customer = db.query(Customer).filter(Customer.id == cid).first()
    if db_customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer Id not found')
    return db_customer


def getAll(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Customer).offset(skip).limit(limit).all()


def add(db: Session, cust: CustomerSchema):
    email = cust.email
    service.checkExistingEmail(db, email)
    data = Customer(
        first_name=cust.first_name,
        last_name=cust.last_name,
        address=cust.address,
        phone_no=cust.phone_no,
        email=cust.email,
    )
    db.add(data)
    db.commit()
    db.refresh(data)


def update(db: Session, cust: CustomerSchema, cid: int):
    db_customer = get(db, cid)
    service.checkExistingEmail(db, cust.email)
    db_customer.first_name = cust.first_name
    db_customer.last_name = cust.last_name
    db_customer.address = cust.address
    db_customer.phone_no = cust.phone_no
    db_customer.email = cust.email

    db.add(db_customer)
    db.commit()


def delete(db: Session, cid: int):
    try:
        data = get(db, cid)
        db.delete(data)
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer id not found')


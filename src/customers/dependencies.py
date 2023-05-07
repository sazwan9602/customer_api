from .schema import Customer as CustomerSchema
from .models import Customer
from . import service
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def get(db: Session, cid: int):
    """
    Get details of a customer information
    :param db: database session
    :param cid: Unique id of a customer info
    :return: if exist, return a customer details
    """
    db_customer = db.query(Customer).filter(Customer.id == cid).first()
    if db_customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer Id not found')
    return db_customer


def getAll(db: Session, skip: int = 0, limit: int = 10):
    """
    Get all customer details in form of list
    :param db: database session
    :param skip: offset start from n row
    :param limit: length of list
    :return: list of customers
    """
    return db.query(Customer).offset(skip).limit(limit).all()


def add(db: Session, cust: CustomerSchema):
    """
    Add new customer into db
    Check for any existing email before commit
    :param db: database session
    :param cust: customer schema
    """
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
    """
    Update any existing customer by given id in parameter
    Check for any existing email before commit
    :param db: database session
    :param cust: customer schema
    :param cid: customer unique id
    """
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
    """
    Completely delete customer details by give id in parameter
    :param db: database session
    :param cid: customer unique id
    """
    try:
        data = get(db, cid)
        db.delete(data)
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer id not found')


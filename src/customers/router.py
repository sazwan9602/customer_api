from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database import getDb
from src.schema import Response
from .schema import Customer
from . import dependencies as CustomerController
from src.auth import dependencies as AuthController

router = APIRouter(dependencies=[Depends(AuthController.getCurrentActiveUser)])
# router = APIRouter()


@router.get('/customer/{cid}', status_code=status.HTTP_200_OK)
async def getCustomer(cid: int, db: Session = Depends(getDb)):
    data = CustomerController.get(db, cid)
    return Response(status='OK', message='_', result=data).dict(exclude_none=True)


@router.post('/customer/add', status_code=status.HTTP_201_CREATED)
async def customerAdd(cust: Customer, db: Session = Depends(getDb)):
    CustomerController.add(db, cust)
    return Response(status='OK', message='new customer created', result=None).dict(exclude_none=True)


@router.put('/customer/update/{cid}', status_code=status.HTTP_201_CREATED)
async def customerUpdate(cid: int, cust: Customer, db: Session = Depends(getDb)):
    CustomerController.update(db, cust, cid)
    return Response(status='OK', message='customer updated', result=None).dict(exclude_none=True)


@router.delete('/customer/delete/{cid}', status_code=status.HTTP_200_OK)
async def customerDelete(cid: int, db: Session = Depends(getDb)):
    CustomerController.delete(db, cid)
    return Response(status='OK', message='customer deleted', result=None).dict(exclude_none=True)


@router.get('/customers', status_code=status.HTTP_200_OK)
async def customerList(skip: int = 0, limit: int = 10, db: Session = Depends(getDb)):
    data = CustomerController.getAll(db, skip, limit)
    return Response(status='OK', message='_', result=data).dict(exclude_none=True)

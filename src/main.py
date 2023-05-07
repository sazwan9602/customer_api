from fastapi import FastAPI
from src.auth import router as Auth
from src.customers import router as Customer
from . import config
from . import database


app = FastAPI()
app.include_router(Auth.router)
app.include_router(Customer.router)


@app.on_event('startup')
async def startup():
    check_conn = database.check_db_connection()
    if check_conn:
        # create tables in db
        config.createAllModels()


@app.get('/')
async def root():
    return {
        'message': 'AHAM Coding Test',
        'API Docs': 'http://127.0.0.1:8000/docs'
    }


@app.on_event('shutdown')
async def shutdown_event():
    database.close_db_connections()
    print('\tApplication is shutting down')


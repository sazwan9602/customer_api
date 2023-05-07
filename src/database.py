from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
from decouple import config

username = config('DB_USERNAME')
password = config('DB_PASSWORD')
host = config('DB_HOST')
port = config('DB_PORT')
db_name = config('DATABASE_NAME')

DATABASE_URL = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def check_db_connection():
    try:
        conn = engine.connect()
        conn.execute(text('SELECT 1'))
        print('\tDatabase connection established')
        conn.close()
        return True
    except Exception as e:
        print('\tError connecting to the database:', e)
        return False


def close_db_connections():
    engine.dispose()
    print('\tDatabase connection closed.')


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

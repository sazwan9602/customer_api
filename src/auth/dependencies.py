from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.users.schema import UserInDB
from decouple import config
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import timedelta, datetime
from .schema import TokenData

SECRET_KEY = config("SECRET")
ALGORITHM = config("ALGORITHM")

db = {
    "admin": {
        "username": "admin",
        "full_name": "admin admin",
        "email": "admin@example.com",
        "hashed_password": "$2b$12$m0rZwujynnREPlYeky8tguAVNMaLzhxp0Rkj.dgyG.IUty45ofmau",
        "disabled": False,
    }
}
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

app = APIRouter()


def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def getPasswordHashed(password):
    return pwd_context.hash(password)


def getUser(db, username):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)


def authenticateUser(db, username: str, password: str):
    user = getUser(db, username)
    if not user:
        return False
    if not verifyPassword(password, user.hashed_password):
        return False

    return user


def createAccessToken(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'expire': str(expire)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def getCurrentUser(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail='could not validate credentials',
                                         headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = getUser(db, username=token_data.username)
    if user is None:
        raise credential_exception

    return user


async def getCurrentActiveUser(current_user: UserInDB = Depends(getCurrentUser)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='inactive user')
    return current_user

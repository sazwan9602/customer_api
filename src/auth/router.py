from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException, status
from .schema import Token
from . import dependencies as AuthController
from datetime import timedelta
from decouple import config

EXPIRES = int(config('TOKEN_EXPIRY'))

router = APIRouter()


@router.post('/auth/token', status_code=status.HTTP_200_OK, response_model=Token)
async def tokenGenerate(form_data: OAuth2PasswordRequestForm = Depends()):
    user = AuthController.authenticateUser(AuthController.db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='incorrect username/password',
                            headers={'WWW-Authenticate': 'Bearer'})
    access_token_expires = timedelta(minutes=EXPIRES)
    access_token = AuthController.createAccessToken(data={'sub': user.username}, expires_delta=access_token_expires)

    return {'access_token': access_token, 'token_type': 'bearer'}

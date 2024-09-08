from datetime import datetime, timedelta, timezone
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from models import CreateUserRequest, Token, Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt


# router setting
router = APIRouter(prefix="/auth", tags=['auth'])

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_barerer = OAuth2PasswordBearer(tokenUrl='auth/token')

# JWT Settings
SECRET_KEY = 'KEY'
ALGORITHM = 'HS256'


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# 의존성 주입
db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False

    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expries_delta: timedelta):
    encode = {
        'sub': username,
        'id': user_id,
    }
    expires = datetime.now(timezone.utc) + expries_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_barerer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not valid user")
        return {'username': username, 'user_id': user_id}
    except JWTError:
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not valid user")
        return {'username': username, 'user_id': user_id}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not valid user")

    token = create_access_token(
        user.username, user.id, timedelta(milliseconds=20))
    return {'access_token': token, 'token_type': 'Barerer'}

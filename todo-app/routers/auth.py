from typing_extensions import Annotated
from fastapi import APIRouter, Depends
from models import CreateUserRequest, Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

# router setting
router = APIRouter(prefix="/auth", tags=['auth'])

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


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

    return True


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hased_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Faild Authentication'
    return 'Success Authentication'

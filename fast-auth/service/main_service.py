from models.user_model import User, RequestUser, ResponseUser
from db import session
import bcrypt
from error import *
from auth import encode_token


def login(user_name, user_password):
    user = session.query(User).filter(
        User.user_name == user_name).first()

    if user == None:
        NoSuchUserException()

    if not checkpw(user_password, user.password):
        WrongPasswordException()

    token = encode_token(user_name)
    return {
        "user_name": user_name,
        "token": token
    }


def create_user(create_user: RequestUser) -> ResponseUser:
    user = session.query(User).filter(
        User.user_name == create_user.user_name).first()

    if not user == None:
        AlreadyExistUsernameException()

    new_user = User(user_name=create_user.user_name,
                    password=encrypt(create_user.password))
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return ResponseUser(id=new_user.id, user_name=new_user.user_name)


def encrypt(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def checkpw(pw_user, pw_db) -> bool:
    return bcrypt.checkpw(pw_user.encode("utf-8"), pw_db.encode("utf-8"))

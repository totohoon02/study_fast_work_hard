from models.user_model import User, RequestUser, ResponseUser
from db import session
import bcrypt
from error import *


def get_users() -> list[ResponseUser]:
    users = session.query(User).all()
    return [ResponseUser(id=user.id, user_name=user.user_name) for user in users]


def get_user_by_id(user_id: int) -> ResponseUser:
    user = session.query(User).filter(User.id == user_id).first()
    if user == None:
        NoSuchUserException()
    return ResponseUser(id=user.id, user_name=user.user_name)


def get_user_by_name(user_name: str) -> ResponseUser:
    user = session.query(User).filter(User.user_name == user_name).first()
    if user == None:
        NoSuchUserException()
    return ResponseUser(id=user.id, user_name=user.user_name)


def update_user_password(update_user: RequestUser) -> ResponseUser:
    user = session.query(User).filter(
        User.user_name == update_user.user_name).first()

    if user == None:
        NoSuchUserException()

    user.password = encrypt(update_user.password)
    session.commit()
    return ResponseUser(id=user.id, user_name=user.user_name)


def delete_user(delete_user: RequestUser) -> ResponseUser:
    user = session.query(User).filter(
        User.user_name == delete_user.user_name).first()

    if user == None:
        NoSuchUserException()

    if not checkpw(delete_user.password, user.password):
        WrongPasswordException()

    session.delete(user)
    session.commit()
    return ResponseUser(id=user.id, user_name=user.user_name)


# jwt 도입후 토큰 체크하는 걸로 변경
def encrypt(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def checkpw(pw_user, pw_db) -> bool:
    return bcrypt.checkpw(pw_user.encode("utf-8"), pw_db.encode("utf-8"))

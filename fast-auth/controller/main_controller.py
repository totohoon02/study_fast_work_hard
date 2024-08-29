from fastapi import APIRouter
from service import main_service as service
from models.user_model import RequestUser, ResponseUser

router = APIRouter(prefix="", tags=["MAIN"])


@router.post("/signup")
def login(request: RequestUser) -> ResponseUser:
    return service.create_user(request)


# 로그인은 post로 바디 넣어서
@router.post("/login")
def login(request: RequestUser):
    return service.login(request)

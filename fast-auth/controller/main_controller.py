from fastapi import APIRouter
from service import main_service as service
from models.user_model import RequestUser, ResponseUser

router = APIRouter(prefix="", tags=["MAIN"])


@router.post("/signup")
def login(request: RequestUser) -> ResponseUser:
    return service.create_user(request)


@router.get("/login")
def login(user_name, user_password):
    return service.login(user_name, user_password)

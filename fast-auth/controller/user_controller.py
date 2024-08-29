from fastapi import APIRouter, Request
from models.user_model import RequestUser, ResponseUser
from service import user_service
from auth import is_valid_token
from error import JwtTokenExpiredException
router = APIRouter(prefix="/users", tags=["USER"])

@router.get("/")
async def get_users(request: Request) -> list[ResponseUser]:
    if not is_valid_token(request.headers.get('X-authorization')):
        raise JwtTokenExpiredException()
    return user_service.get_users()


@router.get("/{user_id}")
async def get_user_by_id(user_id: int) -> ResponseUser:
    return user_service.get_user_by_id(user_id)


@router.post("/")
async def create_user(user: RequestUser) -> ResponseUser:
    return user_service.create_user(user)


@router.put("/")
async def update_user_password(user: RequestUser) -> ResponseUser:
    return user_service.update_user_password(user)


@router.delete("/")
async def delete_users(user: RequestUser) -> ResponseUser:
    return user_service.delete_user(user)

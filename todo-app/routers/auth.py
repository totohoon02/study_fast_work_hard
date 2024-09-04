from fastapi import APIRouter

# router setting
router = APIRouter(prefix="/auth", tags=['auth'])

@router.get("/")
async def get_user():
    return {"user": "authneticated"}
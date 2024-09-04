from fastapi import Depends, HTTPException, Path
from fastapi import APIRouter
from models import Todos, TodoRequest
from typing_extensions import Annotated 
from starlette import status
from database import session
from sqlalchemy.orm import Session


router = APIRouter(prefix="/todos", tags=['todos'])


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# 의존성 주입
db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/")
# Depends: pre-execute
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_id
    raise HTTPException(status_code=404, detail="Todo Not Exist")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, request: TodoRequest):
    todo_model = Todos(**request.model_dump())
    db.add(todo_model)
    db.commit()


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0)
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="not found")
    todo_model.title = todo_request.title
    todo_model.desc = todo_request.desc
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    db: db_dependency,
    todo_id: int = Path(gt=0)
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    db.delete(todo_model)
    db.commit()
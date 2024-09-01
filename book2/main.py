from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from starlette import status
app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    desc: str
    rating: float
    publish_date: datetime

    def __init__(self, id, title, author, desc, rating, publish_date) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.desc = desc
        self.rating = rating
        self.publish_date = publish_date


class BookResquest(BaseModel):
    id: Optional[int] = Field(description="db id auto gen", default=None)
    title: str = Field(min_length=3)  # 각 필드의 validation
    author: str
    desc: str
    rating: float
    publish_date: datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "cfffs",
                "author": 'rro',
                "desc": 'nice book',
                "rating": 4.5,
                "publish_date": datetime.now()
            }
        }
    }


BOOKS = [
    Book(id=1, title="cs", author='rro',
         desc='nice book', rating=4.5, publish_date=datetime.now()),
    Book(id=2, title="cxvs", author='rxzcvro',
         desc='nisdagce book', rating=4.0, publish_date=datetime.now()),
    Book(id=3, title="casds", author='rrasdgo',
         desc='nicezxcb fbook', rating=3.5, publish_date=datetime.now()),
    Book(id=4, title="cqwes", author='rrzxcbo',
         desc='nice bsadook', rating=2.5, publish_date=datetime.now()),
]


@app.get("/books", status_code=status.HTTP_200_OK)  # 구체적인 스테이터스 코드 작성하기
def all_books():
    return BOOKS


@app.post("/books")
def add_book(request: BookResquest):  # validation
    new_book = Book(**request.model_dump())
    BOOKS.append(new_book)


@app.get("/books/{book_id}")
async def get_book(book_id: int = Path(gt=0)):  # Pathparameter Validation
    for book in BOOKS:
        if book.id == book_id:
            return book
    return HTTPException(status_code=404, detail="Item not Found")


@app.get("/books/")
# queryparameter validation
async def read_book_by_rating(rating: float = Query(ge=0.0, le=5.0)):
    books = []
    for book in BOOKS:
        if book.rating >= rating:
            books.append(book)
    return books


@app.put("/books/")
async def update_book(book: BookResquest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            return BOOKS[i]


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break


@app.get("/books/publish")
async def filter_by_date(date: datetime):
    rt_books = []
    for book in BOOKS:
        if book.publish_date == date:
            rt_books.append(book)
    print(rt_books)
    return rt_books

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)

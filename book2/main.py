from fastapi import FastAPI, Body

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    desc: str
    rating: float

    def __init__(self, id, title, author, desc, rating) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.desc = desc
        self.rating = rating


BOOKS = [
    Book(id=1, title="cs", author='rro',
         desc='nice book', rating=4.5),
    Book(id=2, title="cxvs", author='rxzcvro',
         desc='nisdagce book', rating=4.0),
    Book(id=3, title="casds", author='rrasdgo',
         desc='nicezxcb fbook', rating=3.5),
    Book(id=4, title="cqwes", author='rrzxcbo',
         desc='nice bsadook', rating=2.5),
]


@app.get("/books")
def all_books():
    return BOOKS


@app.post("/books")
def add_book(request=Body()):
    BOOKS.append(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)

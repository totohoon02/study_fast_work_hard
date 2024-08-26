from fastapi import Body, FastAPI

app = FastAPI()


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get("/books")
async def read_all_books():
    return BOOKS

# 정적 파라미터 먼저
@app.get("/books/mybook")
async def read_my_book():
    return {'title': 'Mybook', 'author': 'Author Two', 'category': 'math'}

# path parameter
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    # .casefold() : 문자열을 소문자로 변환
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

# query parameters
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# Get all books from a specific author using path or query parameters
@app.get("/books/byauthor/")
async def read_books_by_author_path(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()): # 통과는 되지만 에러처리 안됨.
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

"""
1. Create a new API Endpoint that can fetch all books from a specific author 
using either Path Parameters or Query Parameters.
"""
@app.get("/books/byauthor/{author}")
def get_author_books(author, author_query):
    books = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold() \
                or book.get("author").casefold() == author_query.casefold():
            books.append(book)
    return books


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000)
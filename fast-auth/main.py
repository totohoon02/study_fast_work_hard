from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from controller import main_controller, user_controller
from db import init_db

# create App
app = FastAPI()

# init db
init_db()

# include router
app.include_router(main_controller.router)
app.include_router(user_controller.router)

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)

from fastapi import FastAPI # type: ignore
from . import models
from .database import engine
from .routers import post, user, auth, vote # type: ignore
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# try:
#     conn = psycopg.connect(host='localhost', user='postgres', dbname='fastapi',
#                              password='mysecretpassword', row_factory=dict_row)
#     cursor = conn.cursor()
#     print ("Database connaction was successfuly")

# except Exception as error :
#     print ("Connecting to database faild")
#     print (error)


# def find_post(id):
#     #using psycopg : 
#     cursor.execute(f""" 
#     SELECT * FROM posts WHERE id={id};
#     """,)
#     return cursor.fetchone()

# @app.get("/")
# def root():
#     return {"message": "welcome to my api"}




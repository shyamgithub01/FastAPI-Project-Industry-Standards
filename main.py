
from fastapi import FastAPI
from router import user , post , auth , vote
from fastapi.middleware.cors import CORSMiddleware
from db.database import Base, engine
from models import model

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def root():
    return {"message": "Welcome to my website"}



app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)

app.include_router(vote.router)









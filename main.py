
from fastapi import FastAPI
from router import user , post , auth , vote
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



@app.get('/')
def root():
    return {"message": "Welcome to my website"}

origins = [
    "https://www.google.com"  # allow requests from google.com console
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)

app.include_router(vote.router)









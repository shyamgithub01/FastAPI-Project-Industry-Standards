
from fastapi import FastAPI
from router import user , post , auth , vote
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



@app.get('/')
def root():
    return {"message": "Welcome to my website"}



app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)

app.include_router(vote.router)









from fastapi import APIRouter, HTTPException, status, Depends
from schemas import post , vote 
from db import database
from sqlalchemy.orm import Session
from models import posts , votes ,users
from utils import oauth2
from typing import List



router = APIRouter(tags=["Post"])

from sqlalchemy import func
from sqlalchemy.orm import aliased
from schemas.post import PostWithVotes  # new schema for vote data

@router.get("/posts", response_model=List[post.PostOut])
def get_posts(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = (
        db.query(posts.Post, func.count(votes.Vote.post_id).label("votes"))
        .join(users.Users, users.Users.id == users.Post.owner_id)
        .outerjoin(votes.Vote, votes.Vote.post_id == posts.Post.id)
        .group_by(posts.Post.id, users.Users.id)
        .all()
    )

   
    results = []
    for post, vote_count in posts:
        post_dict = post.__dict__.copy()
        post_dict["votes"] = vote_count
        post_dict["owner"] = post.owner  
        results.append(post_dict)

    return results

# Create a new post
@router.post("/posts", response_model=post.Post, status_code=status.HTTP_201_CREATED)
def create_post(post_data: post.CreatePost, db: Session = Depends(database.get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = posts.Post(owner_id=current_user.id , **post_data.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get a single post by ID
@router.get('/posts/{id}', response_model=post.Post)
def get_one_post(id: int, db: Session = Depends(database.get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    post_item = db.query(posts.Post).filter(posts.Post.id == id).first()
    if post_item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_item

# Delete a post by ID
@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: users.Users = Depends(oauth2.get_current_user)
):
    post_item = db.query(posts.Post).filter(posts.Post.id == id).first()

    if post_item is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if post_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    db.delete(post_item)
    db.commit()
    return None


# Update a post by ID
@router.put('/posts/{id}', response_model=post.Post)
def update_post(id: int, updated_data: post.CreatePost, db: Session = Depends(database.get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(posts.Post).filter(posts.Post.id == id)
    post_item = post_query.first()
    if post_item is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
 
    post_query.update(updated_data.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post_item)
    return post_item

from fastapi import FastAPI , status , HTTPException , Depends , APIRouter
from db import database
from sqlalchemy.orm import Session
from schemas.vote import Vote
from models import model
from schemas import vote
from utils import oauth2

router = APIRouter(
    tags=["Vote"]

)
  
@router.post('/vote', status_code=status.HTTP_201_CREATED)
def vote(
    vote: Vote,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    # ✅ Step 1: Check if the post exists
    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist"
        )

    # ✅ Step 2: Check if user has already voted
    vote_query = db.query(model.Vote).filter(
        model.Vote.post_id == vote.post_id,
        model.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    # ✅ Step 3: Handle vote/unvote
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already voted on this post"
            )
        new_vote = model.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote removed successfully"}

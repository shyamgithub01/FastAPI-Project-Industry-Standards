from fastapi import  status , HTTPException , Depends , APIRouter
from db import database
from sqlalchemy.orm import Session
from schemas.vote import Vote
from models import votes ,posts
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
    
    post = db.query(posts.Post).filter(posts.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} does not exist"
        )

    
    vote_query = db.query(votes.Vote).filter(
        votes.Vote.post_id == vote.post_id,
        votes.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already voted on this post"
            )
        new_vote = votes.Vote(post_id=vote.post_id, user_id=current_user.id)
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

# post endpoint to give vote to a post vote_post
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
from ..database import get_db
from ..models import Post, User, Vote

router = APIRouter(
    prefix="/v1/votes",
    tags=["Votes"]
)

@router.post("/", response_model=schemas.Vote, status_code=status.HTTP_201_CREATED)
def vote_post(db: Session = Depends(get_db), vote: schemas.Vote = Depends(schemas.Vote), current_user: User = Depends(oauth2.get_current_user)):
    """
    Cast a vote on a post.

    This endpoint allows users to cast a vote on a post. The vote details are passed
    in the request body as a JSON object. The vote is stored in the database and
    the vote ID is returned.

    Parameters:
    - db (Session): The database session, automatically injected.
    - vote (schemas.Vote): The vote details, automatically injected.
    - current_user (User): The currently authenticated user, automatically injected.

    Returns:
    - schemas.Vote: The created vote.

    Raises:
    - HTTPException: If the post does not exist, a 404 error is raised.
    - HTTPException: If the user has already voted on the post, a 409 error is raised.
    - HTTPException: If the vote is not found, a 404 error is raised.
    - HTTPException: If there is a database error, a 500 error is raised.

    Example:
    POST /v1/votes
    {
        "post_id": 1,
        "direction": 1
    }
    """
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    check_if_exists(post, vote.post_id)
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.owner_id == current_user.id)
    found_vote = vote_query.first()
    if vote.direction == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already voted on this post")
        new_vote = models.Vote(owner_id=current_user.id, post_id=vote.post_id, dir=vote.dir)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    else:
        if found_vote is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
        db.delete(found_vote)
        db.commit()
        return {"message": "Vote deleted successfully"}

def check_if_exists(post, post_id):
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")
# 1. get_posts(db: Session, limit: int, skip: int)
# 2. get_post(db: Session, post_id: int)
# 3. create_post(db: Session, post: CreatePost)
# 4. update_post(db: Session, post_id: int, post: CreatePost)
# 5. delete_post(db: Session, post_id: int)

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models, utils, oauth2
from ..database import get_db
from ..models import Post, User


router = APIRouter(
    prefix="/v1/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = "",
              current_user: User = Depends(oauth2.get_current_user)):
    """
    Retrieve a list of posts from the database.

    This endpoint allows users to fetch posts with optional pagination and search functionality. 
    It returns a list of posts along with the count of votes associated with each post.

    Parameters:
    - db (Session): The database session, automatically injected.
    - limit (int): The maximum number of posts to return (default is 10).
    - skip (int): The number of posts to skip for pagination (default is 0).
    - search (Optional[str]): A search term to filter posts by title (default is an empty string).
    - current_user (User): The currently authenticated user, automatically injected.

    Returns:
    - List[schemas.PostOut]: A list of posts, each including the post details and associated vote count.

    Example:
    GET /posts?limit=5&skip=0&search=example
    """
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.title.contains(search)) \
        .offset(skip) \
        .limit(limit) \
        .all()
    return results

@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(db: Session = Depends(get_db), post_id: int = Path(..., ge=1), current_user: User = Depends(oauth2.get_current_user)):
    """
    Retrieve a single post by its ID from the database.

    This endpoint allows users to fetch a specific post along with the count of votes associated with it. 
    If the post does not exist, a 404 error is returned.

    Parameters:
    - db (Session): The database session, automatically injected.
    - post_id (int): The ID of the post to retrieve (must be greater than or equal to 1).
    - current_user (User): The currently authenticated user, automatically injected.

    Returns:
    - schemas.PostOut: The post details along with the associated vote count.

    Raises:
    - HTTPException: If the post with the specified ID is not found, a 404 error is raised.

    Example:
    GET /posts/1
    """
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.id == post_id) \
        .first()
    check_if_exists(post, post_id)
    return post




def check_if_exists(post, post_id):
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")


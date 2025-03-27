# 1. get_posts(db: Session, limit: int, skip: int)
# 2. get_post(db: Session, post_id: int)
# 3. create_post(db: Session, post: CreatePost)
# 4. update_post(db: Session, post_id: int, post: CreatePost)
# 5. delete_post(db: Session, post_id: int)
# Interview Question: Difference between Column wise operations and Row wise operations in the Database.
# When we need row wise operations and when column wise operations?

from fastapi import APIRouter, Depends, status, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models, utils, oauth2
from ..database import get_db
from ..models import Post, User
from sqlalchemy import func



router = APIRouter(
    prefix="/v1/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: schemas.TokenData = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.title.contains(search)) \
        .offset(skip) \
        .limit(limit) \
        .all()
    
    # Convert results to list of PostOut schema
    posts = []
    for post, votes in results:
        # Convert owner to dictionary
        owner = {
            "id": post.owner.id,
            "email": post.owner.email,
            "created_at": post.owner.created_at
        }
        
        # Create the Post schema
        post_schema = schemas.Post(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            created_at=post.created_at,
            owner_id=post.owner_id,
            owner=owner
        )
        
        # Create the PostOut schema
        post_data = schemas.PostOut(
            Post=post_schema,
            votes=votes
        )
        
        posts.append(post_data)
    
    return posts

@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(db: Session = Depends(get_db), 
             post_id: int = Path(..., ge=1), 
             current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.id == post_id) \
        .first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} was not found"
        )
    
    # Convert owner to dictionary
    owner = {
        "id": post.Post.owner.id,
        "email": post.Post.owner.email,
        "created_at": post.Post.owner.created_at
    }
    
    # Create the Post schema
    post_schema = schemas.Post(
        id=post.Post.id,
        title=post.Post.title,
        content=post.Post.content,
        published=post.Post.published,
        created_at=post.Post.created_at,
        owner_id=post.Post.owner_id,
        owner=owner
    )
    
    # Create and return the PostOut schema
    post_data = schemas.PostOut(
        Post=post_schema,
        votes=post.votes
    )
    
    return post_data




@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(db: Session = Depends(get_db), post: schemas.PostCreate = Depends(schemas.PostCreate), current_user: User = Depends(oauth2.get_current_user)):
    """
    Create a new post in the database.

    This endpoint allows users to create new posts. The post details are passed
    in the request body as a JSON object. The post is created in the database and
    the post ID is returned.

    Parameters:
    - db (Session): The database session, automatically injected.
    - post (schemas.CreatePost): The post details, automatically injected.
    - current_user (User): The currently authenticated user, automatically injected.

    Returns:
    - schemas.Post: The created post.

    Raises:
    - HTTPException: If there is a database error, a 500 error is raised.

    Example:
    POST /posts
    {
        "title": "My First Post",
        "content": "This is the first post",
        "published": true
    }
    """
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(db: Session = Depends(get_db), post_id: int = Path(..., ge=1), post: schemas.PostCreate = Depends(schemas.PostCreate), current_user: User = Depends(oauth2.get_current_user)):
    """
    Update an existing post in the database.

    This endpoint allows users to update existing posts. The post ID is passed as a path
    parameter and the updated post details are passed in the request body as a JSON object.
    The post is updated in the database and the post ID is returned.

    Parameters:
    - db (Session): The database session, automatically injected.
    - post_id (int): The post ID, passed as a path parameter.
    - post (schemas.CreatePost): The updated post details, automatically injected.
    - current_user (User): The currently authenticated user, automatically injected.

    Returns:
    - schemas.Post: The updated post.

    Raises:
    - HTTPException: If there is a database error, a 500 error is raised.
    - HTTPException: If the post does not exist, a 404 error is raised.
    - HTTPException: If the authenticated user is not the owner of the post,
      a 403 error is raised.

    Example:
    PUT /posts/1
    {
        "title": "My First Post",
        "content": "This is the first post",
        "published": true
    }
    """
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    found_post = post_query.first()
    check_if_exists(found_post, post_id)
    if found_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()




@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(db: Session = Depends(get_db), post_id: int = Path(..., ge=1), current_user: User = Depends(oauth2.get_current_user)):
    """
    Delete an existing post from the database.

    This endpoint allows users to delete existing posts. The post ID is passed as a path
    parameter. The post is deleted from the database and a 204 No Content response is returned.

    Parameters:
    - db (Session): The database session, automatically injected.
    - post_id (int): The post ID, passed as a path parameter.
    - current_user (User): The currently authenticated user, automatically injected.

    Returns:
    - None: A 204 No Content response is returned.

    Raises:
    - HTTPException: If there is a database error, a 500 error is raised.
    - HTTPException: If the post does not exist, a 404 error is raised.
    - HTTPException: If the authenticated user is not the owner of the post,
      a 403 error is raised.

    Example:
    DELETE /posts/1
    """
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    found_post = post_query.first()
    check_if_exists(found_post, post_id)
    if found_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def check_if_exists(post, post_id):
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found")


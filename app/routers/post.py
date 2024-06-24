from fastapi import FastAPI,Response,status, HTTPException, Depends, APIRouter # type: ignore
from typing import List, Optional
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import func
from .. import schemas, models
from ..database import get_db
from .. import oauth2


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
@router.get("/",response_model= List[schemas.PostOut])
# @router.get("/")
def get_posts(response:Response ,db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), Limit: int = 10, Skip: int = 0, Search: Optional[str] = ""):

    # posts = db.query(models.Post).filter(models.Post.title.contains(Search)).limit(Limit).offset(Skip)

    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(Search)).limit(Limit).offset(Skip).all()
        
    response.status_code = 200
    return posts

@router.post("/", response_model= schemas.Post)
def create_post(post:schemas.PostCreate, response:Response, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #psycopg :
    # cursor.execute("""
    # INSERT INTO posts (title,content,published)
    # VALUES (%s, %s, %s) RETURNING *;
    # """, (post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()
    #----------------------------------------------------
    #sqlAlchemy :
    new_post = models.Post(user_id=current_user.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    response.status_code = 201
    return new_post


@router.get("/{id}",response_model= schemas.PostOut) # path paramitar.
def get_post (id: int, response:Response, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    # post = find_post(id)



    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        # response.status_code = 404
        # or response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = {"message":f"post with id {id} was not found"})
    else :
        # print(post.user.email)
        return post



@router.delete("/{id}")
def delete_post(id : int, response: Response, db : Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #psycopg : 
    # cursor.execute(f""" 
    #     DELETE FROM posts WHERE id = {id} returning *;
    # """)
    # post = cursor.fetchone()
    # if post == None:
    #     raise HTTPException(status_code = 404, detail = f"Post with id {id} was not found")
    
    # conn.commit()
    #----------------------------------------------------------------------------------------
    #sqlAlchemy :
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = 404, detail = f"Post with id {id} was not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to preform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    response.status_code = 204
    return Response(status_code = status.HTTP_204_NO_CONTENT)



@router.put("/{id}",response_model= schemas.Post)
def update_post(id : str, updated_post:schemas.PostCreate, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #psycopg : 
    # cursor.execute(""" 
    # UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s returning *;
    # """, (updated_post.title,updated_post.content,updated_post.published, id))

    # post = cursor.fetchone()

    # if post == None:
    #     raise HTTPException(status_code = 404, detail = f"Post with id {id} was not found")

    # conn.commit()
    #----------------------------------------------------------------------------------------
    #sqlAlchemy : 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = 404, detail = f"Post with id {id} was not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to preform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
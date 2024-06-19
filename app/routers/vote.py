from fastapi import FastAPI,Response,status, HTTPException, Depends, APIRouter # type: ignore
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, )
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} doesn't exist!")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_voit = vote_query.first()

    if (vote.dir == 1):
        if found_voit:
            print(vote_query)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"user {current_user.id} id has alredy voted on post {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfuly added vote"}
    else:
        if not found_voit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfuly deleted voie"}


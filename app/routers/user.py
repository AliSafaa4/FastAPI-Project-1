from fastapi import FastAPI,Response,status, HTTPException, Depends , APIRouter # type: ignore
from typing import Optional, List
from sqlalchemy.orm import Session # type: ignore
from .. import schemas, utils, models
from ..database import engine, get_db

router = APIRouter(
     prefix="/users",
     tags=['Users']
)

@router.post("/", response_model = schemas.UserResponse)
def create_user(userdet:schemas.UserCreate, db : Session = Depends(get_db)):
        
        hashed_password = utils.hash(userdet.password)
        userdet.password = hashed_password

        new_user = models.User(**userdet.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist.")

    return user
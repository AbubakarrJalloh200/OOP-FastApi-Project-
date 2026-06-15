from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..database import get_db
from .. import models, schemas, crud
from ..auth import verify_password, create_access_token

router = APIRouter()

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": f"User with id {user_id} deleted successfully"}

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}


from sqlalchemy.orm import Session
from . import models, schemas
from .auth import hash_password


def create_user(db: Session, user: schemas.UserCreate):
    hashed = hash_password(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(**job.dict())

    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return db_job
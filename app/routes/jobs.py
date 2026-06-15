from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import asyncio

from ..database import get_db
from ..models import Job
from ..schemas import JobCreate, JobResponse, JobUpdate
from ..auth import get_current_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/", response_model=JobResponse)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.get("/", response_model=List[JobResponse])
async def get_jobs(db: Session = Depends(get_db)):
    await asyncio.sleep(1)  # async demonstration
    return db.query(Job).all()


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    updated: JobUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    for key, value in updated.dict().items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)

    return job


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()

    return {"message": "Job deleted"}
from fastapi import FastAPI
from .database import Base, engine
from .routes import users, jobs

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Opportunity API",
    description="Youth Employment Listings API",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(jobs.router)


@app.get("/")
def home():
    return {"message": "Job API is running"}
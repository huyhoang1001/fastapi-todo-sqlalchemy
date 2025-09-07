from fastapi import FastAPI
from app.core.database import engine
from app.models import user, company, task
from app.routers import auth, users, companies, tasks

# Create database tables
user.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API", version="1.0.0")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(companies.router, prefix="/companies", tags=["companies"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Todo API"}
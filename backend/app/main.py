from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, tasks

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="A simple Task Manager REST API with JWT Authentication",
    version="1.0.0"
)

# CORS — allows frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Task Manager API is running 🚀"}
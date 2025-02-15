from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine
from app.db import models
from app.api.routes.data_routes import router as data_router
from app.api.routes.wpl_routes import router as wpl_router

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Skye Analytics API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(data_router)
app.include_router(wpl_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Skye Analytics API", "status": "running"}
# app/api/routes/data_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import DataPoint

router = APIRouter()

@router.get("/data/")
def get_data(db: Session = Depends(get_db)):
    data = db.query(DataPoint).all()
    return data

@router.post("/data/")
def create_data(value: float, category: str, source: str, db: Session = Depends(get_db)):
    data_point = DataPoint(value=value, category=category, source=source)
    db.add(data_point)
    db.commit()
    db.refresh(data_point)
    return data_point
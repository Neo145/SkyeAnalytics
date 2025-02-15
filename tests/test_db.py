# F:\SkyeAnalytics\tests\test_db.py
import pytest
from app.db.database import engine, SessionLocal, Base
from app.db.models import DataPoint

def setup_module(module):
    """Initialize the database before running tests"""
    Base.metadata.create_all(bind=engine)

def teardown_module(module):
    """Clean up after tests"""
    Base.metadata.drop_all(bind=engine)

def test_database_connection():
    """Test that we can connect to the database"""
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        assert result.scalar() == 1

def test_create_datapoint():
    """Test creating a data point"""
    db = SessionLocal()
    try:
        # Create test data point
        dp = DataPoint(
            value=42.0,
            category="test",
            source="test"
        )
        db.add(dp)
        db.commit()
        
        # Verify
        assert dp.id is not None
        assert dp.value == 42.0
        
        # Clean up
        db.delete(dp)
        db.commit()
    finally:
        db.close()
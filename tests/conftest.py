# tests/conftest.py
import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure the 'app' module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app, get_db
from app.db.database import Base

# Use in-memory SQLite DB for fast testing
TEST_DB_URL = "sqlite:///:memory:"

# Set up the test database engine and session
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture to set up and tear down the database schema
@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Fixture to override the FastAPI dependency and provide a test client
@pytest.fixture()
def client(test_db):
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.constants import COMPANY_ADMIN_ROLE
from app.core.security import hash_password
from app.db.base import Base
from app.db.session import get_db
from app.models.location import Location
from app.models.user import User
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        location = Location(state="Lagos", city="Ikeja", area_name="Allen Avenue")
        db.add(location)
        db.flush()
        admin = User(
            name="Admin User",
            email="admin@powerpulse.test",
            password_hash=hash_password("password123"),
            role=COMPANY_ADMIN_ROLE,
            location_id=location.id,
        )
        db.add(admin)
        db.commit()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def user_token(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "user@powerpulse.test",
            "password": "password123",
            "location_id": 1,
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "user@powerpulse.test", "password": "password123"},
    )
    return response.json()["access_token"]


@pytest.fixture()
def admin_token(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@powerpulse.test", "password": "password123"},
    )
    return response.json()["access_token"]


import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database.database import Base
from app.main import app, get_db
from app.permissions import permissions
from app.firebase import firebase
from app import main


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)
HACKER = "hacker"

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_check_for_permission(db, firebase_token, clearance):
    if firebase_token == HACKER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="")


def override_is_accessible(db, firebase_token, clearance="player"):
    return True


def override_verify_token(token):
    return str(token)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture()
def restart_db():
    global TestingSessionLocal

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    yield    


@pytest.fixture(autouse=True)
def mock_permissions(monkeypatch):
    monkeypatch.setattr(permissions, 'check_for_permission', override_check_for_permission)
    monkeypatch.setattr(permissions, 'is_accessible', override_is_accessible)
    monkeypatch.setattr(main, 'verify_token', override_verify_token)

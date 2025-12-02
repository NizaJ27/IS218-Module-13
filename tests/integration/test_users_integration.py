import os
import time
import pytest
from fastapi.testclient import TestClient

from main import app
from app.db import init_db


@pytest.fixture(autouse=True)
def setup_db():
    # Ensure tables exist for the configured DATABASE_URL
    # If using the default sqlite file, remove it to start fresh between runs
    try:
        from app.db import DATABASE_URL
        if DATABASE_URL.startswith("sqlite") and "test_db.sqlite" in DATABASE_URL:
            import os

            if os.path.exists("./test_db.sqlite"):
                os.remove("./test_db.sqlite")
    except Exception:
        pass
    init_db()
    yield


def test_register_user_success():
    """Test successful user registration."""
    client = TestClient(app)
    payload = {"username": "testuser1", "email": "testuser1@example.com", "password": "password123"}
    r = client.post("/users/register", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["username"] == "testuser1"
    assert data["email"] == "testuser1@example.com"
    assert "password" not in data
    assert "password_hash" not in data
    assert "id" in data


def test_register_duplicate_user():
    """Test registration with duplicate username/email returns 400."""
    client = TestClient(app)
    payload = {"username": "testuser2", "email": "testuser2@example.com", "password": "password123"}
    r1 = client.post("/users/register", json=payload)
    assert r1.status_code == 200
    
    # Attempt duplicate
    r2 = client.post("/users/register", json=payload)
    assert r2.status_code == 400
    assert "already exists" in r2.json()["detail"].lower()


def test_register_invalid_email():
    """Test registration with invalid email format returns 400."""
    client = TestClient(app)
    payload = {"username": "testuser3", "email": "not-an-email", "password": "password123"}
    r = client.post("/users/register", json=payload)
    assert r.status_code == 400


def test_login_user_success():
    """Test successful user login."""
    client = TestClient(app)
    # First register a user
    register_payload = {"username": "loginuser1", "email": "loginuser1@example.com", "password": "mypassword"}
    client.post("/users/register", json=register_payload)
    
    # Now login
    login_payload = {"username": "loginuser1", "password": "mypassword"}
    r = client.post("/users/login", json=login_payload)
    assert r.status_code == 200
    data = r.json()
    assert data["username"] == "loginuser1"
    assert "password" not in data


def test_login_invalid_username():
    """Test login with non-existent username returns 401."""
    client = TestClient(app)
    login_payload = {"username": "nonexistent", "password": "anypassword"}
    r = client.post("/users/login", json=login_payload)
    assert r.status_code == 401
    response_data = r.json()
    # May return error as string or in detail field depending on exception handler
    assert "invalid" in str(response_data).lower() or "detail" in response_data


def test_login_invalid_password():
    """Test login with wrong password returns 401."""
    client = TestClient(app)
    # Register a user
    register_payload = {"username": "loginuser2", "email": "loginuser2@example.com", "password": "correctpassword"}
    client.post("/users/register", json=register_payload)
    
    # Try to login with wrong password
    login_payload = {"username": "loginuser2", "password": "wrongpassword"}
    r = client.post("/users/login", json=login_payload)
    assert r.status_code == 401
    assert "invalid" in r.json()["detail"].lower()


def test_register_and_uniqueness():
    """Legacy test for backward compatibility."""
    client = TestClient(app)
    payload = {"username": "tester1", "email": "tester1@example.com", "password": "pass123"}
    r = client.post("/users/register", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["username"] == "tester1"
    assert data["email"] == "tester1@example.com"
    assert "password_hash" not in data

    # Attempt duplicate
    r2 = client.post("/users/register", json=payload)
    assert r2.status_code == 400


def test_invalid_email_via_endpoint():
    """Legacy test for backward compatibility."""
    client = TestClient(app)
    payload = {"username": "tester2", "email": "not-an-email", "password": "pass123"}
    r = client.post("/users/register", json=payload)
    # This application maps validation errors to HTTP 400 in the handler
    assert r.status_code == 400

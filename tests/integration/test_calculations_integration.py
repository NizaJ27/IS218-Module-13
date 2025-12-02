import os
import pytest
from fastapi.testclient import TestClient
from app.db import init_db, SessionLocal
from app import schemas, models
from app.operations import calculations as calc_ops
from main import app


@pytest.fixture(autouse=True)
def setup_db():
    try:
        from app.db import DATABASE_URL
        if DATABASE_URL.startswith("sqlite") and "test_db.sqlite" in DATABASE_URL:
            if os.path.exists("./test_db.sqlite"):
                os.remove("./test_db.sqlite")
    except Exception:
        pass
    init_db()
    yield


def test_create_calculation_stores_result():
    """Test creating calculation via database operation."""
    db = SessionLocal()
    try:
        calc_in = schemas.CalculationCreate(a=10, b=5, type=models.CalculationType.DIVIDE)
        calc = calc_ops.create_calculation(db, calc_in, store_result=True)
        assert calc.id is not None
        assert calc.result == 2.0

        # Fetch from DB
        fetched = db.get(models.Calculation, calc.id)
        assert fetched is not None
        assert fetched.result == 2.0
    finally:
        db.close()


def test_create_calculation_invalid_type_raises():
    """Test invalid calculation type raises error."""
    db = SessionLocal()
    try:
        with pytest.raises(ValueError):
            # using a wrong type value should raise when mapping in compute_result
            bad = schemas.CalculationCreate(a=1, b=1, type="NotAType")
            calc_ops.create_calculation(db, bad)
    finally:
        db.close()


# ========== API Integration Tests (BREAD) ==========

def test_add_calculation_via_api():
    """Test Add (POST /calculations) endpoint."""
    client = TestClient(app)
    payload = {"a": 10, "b": 5, "type": "Add"}
    r = client.post("/calculations", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["a"] == 10
    assert data["b"] == 5
    assert data["type"] == "Add"
    assert data["result"] == 15
    assert "id" in data


def test_browse_calculations_via_api():
    """Test Browse (GET /calculations) endpoint."""
    client = TestClient(app)
    # Create some calculations first
    client.post("/calculations", json={"a": 5, "b": 3, "type": "Add"})
    client.post("/calculations", json={"a": 10, "b": 2, "type": "Multiply"})
    
    r = client.get("/calculations")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_read_calculation_via_api():
    """Test Read (GET /calculations/{id}) endpoint."""
    client = TestClient(app)
    # Create a calculation
    create_resp = client.post("/calculations", json={"a": 8, "b": 2, "type": "Divide"})
    calc_id = create_resp.json()["id"]
    
    # Read it back
    r = client.get(f"/calculations/{calc_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == calc_id
    assert data["a"] == 8
    assert data["b"] == 2
    assert data["result"] == 4


def test_read_nonexistent_calculation():
    """Test Read returns 404 for non-existent calculation."""
    client = TestClient(app)
    r = client.get("/calculations/99999")
    assert r.status_code == 404


def test_edit_calculation_via_api():
    """Test Edit (PUT /calculations/{id}) endpoint."""
    client = TestClient(app)
    # Create a calculation
    create_resp = client.post("/calculations", json={"a": 5, "b": 3, "type": "Add"})
    calc_id = create_resp.json()["id"]
    
    # Update it
    update_payload = {"a": 10, "b": 2, "type": "Subtract"}
    r = client.put(f"/calculations/{calc_id}", json=update_payload)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == calc_id
    assert data["a"] == 10
    assert data["b"] == 2
    assert data["type"] == "Sub"
    assert data["result"] == 8


def test_edit_nonexistent_calculation():
    """Test Edit returns 404 for non-existent calculation."""
    client = TestClient(app)
    r = client.put("/calculations/99999", json={"a": 1, "b": 1, "type": "Add"})
    assert r.status_code == 404


def test_delete_calculation_via_api():
    """Test Delete (DELETE /calculations/{id}) endpoint."""
    client = TestClient(app)
    # Create a calculation
    create_resp = client.post("/calculations", json={"a": 7, "b": 3, "type": "Multiply"})
    calc_id = create_resp.json()["id"]
    
    # Delete it
    r = client.delete(f"/calculations/{calc_id}")
    assert r.status_code == 200
    assert "deleted" in r.json()["message"].lower()
    
    # Verify it's gone
    get_resp = client.get(f"/calculations/{calc_id}")
    assert get_resp.status_code == 404


def test_delete_nonexistent_calculation():
    """Test Delete returns 404 for non-existent calculation."""
    client = TestClient(app)
    r = client.delete("/calculations/99999")
    assert r.status_code == 404


def test_create_calculation_division_by_zero():
    """Test that division by zero returns 400 error."""
    client = TestClient(app)
    payload = {"a": 10, "b": 0, "type": "Divide"}
    r = client.post("/calculations", json=payload)
    assert r.status_code == 400
    response_data = r.json()
    # Check for error indication - may be in different formats
    assert "division" in str(response_data).lower() or "zero" in str(response_data).lower() or "error" in str(response_data).lower()


def test_create_calculation_invalid_type():
    """Test that invalid calculation type returns 400 error."""
    client = TestClient(app)
    payload = {"a": 5, "b": 3, "type": "InvalidType"}
    r = client.post("/calculations", json=payload)
    assert r.status_code == 400

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ── Auth Tests ────────────────────────────────────
def test_register():
    res = client.post("/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "test1234"
    })
    assert res.status_code in [201, 400]  # 400 if already exists

def test_login():
    # Register first
    client.post("/register", json={
        "username": "testuser2",
        "email": "test2@test.com",
        "password": "test1234"
    })
    # Then login
    res = client.post("/login", json={
        "email": "test2@test.com",
        "password": "test1234"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_login_wrong_password():
    res = client.post("/login", json={
        "email": "test2@test.com",
        "password": "wrongpassword"
    })
    assert res.status_code == 401

# ── Task Tests ────────────────────────────────────
def get_token():
    client.post("/register", json={
        "username": "taskuser",
        "email": "taskuser@test.com",
        "password": "test1234"
    })
    res = client.post("/login", json={
        "email": "taskuser@test.com",
        "password": "test1234"
    })
    return res.json()["access_token"]

def test_create_task():
    token = get_token()
    res = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Test Description"
    }, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 201
    assert res.json()["title"] == "Test Task"

def test_get_tasks():
    token = get_token()
    res = client.get("/tasks/", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert "tasks" in res.json()

def test_complete_task():
    token = get_token()
    # Create task first
    create_res = client.post("/tasks/", json={
        "title": "Complete Me"
    }, headers={"Authorization": f"Bearer {token}"})
    task_id = create_res.json()["id"]

    # Mark complete
    res = client.put(f"/tasks/{task_id}", json={
        "completed": True
    }, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["completed"] == True

def test_delete_task():
    token = get_token()
    # Create task first
    create_res = client.post("/tasks/", json={
        "title": "Delete Me"
    }, headers={"Authorization": f"Bearer {token}"})
    task_id = create_res.json()["id"]

    # Delete it
    res = client.delete(f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 204

def test_unauthorized_access():
    res = client.get("/tasks/")
    assert res.status_code == 401
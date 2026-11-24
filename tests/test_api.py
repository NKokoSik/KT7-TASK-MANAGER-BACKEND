from app.core.security import create_access_token


def auth_headers(user):
    return {"Authorization": f"Bearer {create_access_token(str(user.id))}"}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_and_login(client):
    registered = client.post(
        "/auth/register",
        json={
            "full_name": "New User",
            "email": "new@example.com",
            "password": "password123",
        },
    )
    assert registered.status_code == 201
    assert registered.json()["email"] == "new@example.com"
    assert "hashed_password" not in registered.json()

    login = client.post(
        "/auth/login",
        data={"username": "new@example.com", "password": "password123"},
    )
    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"
    assert login.json()["access_token"]


def test_duplicate_registration_returns_409(client):
    response = client.post(
        "/auth/register",
        json={
            "full_name": "Duplicate User",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 409


def test_project_and_task_crud(client, monkeypatch):
    monkeypatch.setattr(
        "app.routers.tasks.notify_task_created.delay",
        lambda *args, **kwargs: None,
    )
    headers = auth_headers(client.test_user)
    project = client.post(
        "/projects",
        json={"name": "Course work", "description": "Final project"},
        headers=headers,
    )
    assert project.status_code == 201
    project_id = project.json()["id"]

    task = client.post(
        f"/projects/{project_id}/tasks",
        json={"title": "Prepare API", "status": "todo"},
        headers=headers,
    )
    assert task.status_code == 201
    task_id = task.json()["id"]

    updated = client.patch(
        f"/projects/{project_id}/tasks/{task_id}",
        json={"status": "done"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "done"

    deleted = client.delete(
        f"/projects/{project_id}/tasks/{task_id}",
        headers=headers,
    )
    assert deleted.status_code == 204


def test_project_requires_authentication(client):
    response = client.get("/projects")
    assert response.status_code == 401


def test_admin_route_forbidden_for_regular_user(client):
    response = client.get("/admin/users", headers=auth_headers(client.test_user))
    assert response.status_code == 403


def test_admin_route_allowed_for_admin(client):
    client.test_user.role = "admin"
    client.test_db.commit()
    response = client.get("/admin/users", headers=auth_headers(client.test_user))
    assert response.status_code == 200
    assert any(user["email"] == "test@example.com" for user in response.json())


def test_notification_not_found_returns_404(client):
    response = client.patch(
        "/notifications/999/read",
        headers=auth_headers(client.test_user),
    )
    assert response.status_code == 404

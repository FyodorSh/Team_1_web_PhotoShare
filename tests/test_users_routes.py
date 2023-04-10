import pytest

from src.database.models import User, UserRole

@pytest.fixture()
def user():
    return {
        "username": "deadpool", 
        "email": "deadpool@example.com", 
        "password": "123456789"
        }

@pytest.fixture()
def admin():
    return {
        "username": "test1", 
        "email": "test1@example.com", 
        "password": "testtest", 
        "first_name": "test1",
        "last_name": "test1", 
        "user_role": "Admin"
        }


@pytest.fixture()
def admin_token(admin, client, session):
    client.post("/api/auth/signup", json=admin)
    c: User = session.query(User).filter(User.email == admin['email']).first()
    c.user_role = UserRole.Admin.name
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": admin['email'], "password": admin['password']},
    )
    data = response.json()
    return data["access_token"]


@pytest.fixture()
def token(client, user, session):
    client.post("/api/auth/signup", json=user)
    c: User = session.query(User).filter(User.email == user['email']).first()
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user['email'], "password": user['password']},
    )
    data = response.json()
    return data["access_token"]


def test_get_contacts(client, user):
    response = client.get(
        "/api/users/all",
        json = {"id":"1"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["username"] == user["username"]
    assert "id" in data[0]

def test_get_user_profile(client, user):
    response = client.get(
        f"/api/users/get_user_profile?username={user['username']}]"
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == user["username"]
    assert "id" in data

def test_update_user_self(client, token):
    response = client.put(
        "/api/users/update_user_self",
        json={"first_name": "new_first_name"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == "new_first_name"
    assert "id" in data

def test_update_user_as_admin(client, admin_token):
    response = client.put(
        "/api/users/update_user_as_admin",
        json={"user_role": "User"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["user_role"] == "User"
    assert "id" in data

import pytest
from fastapi import status

class TestUsers:
    def test_create_user(self, client):
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "password": "newpass123",
            "is_active": True
        }
        
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert "password" not in data

    def test_create_user_duplicate_email(self, client, test_user):
        user_data = {
            "email": test_user.email,
            "username": "differentuser",
            "first_name": "Different",
            "last_name": "User",
            "password": "newpass123"
        }
        
        response = client.post("/users/", json=user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_current_user(self, client, test_user, auth_headers):
        response = client.get("/users/me", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == test_user.email
        assert data["username"] == test_user.username

    def test_get_current_user_unauthorized(self, client):
        response = client.get("/users/me")
        
        # HTTPBearer returns 403 when no auth header provided
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_users_admin_only(self, client, admin_headers):
        response = client.get("/users/", headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_get_users_non_admin(self, client, auth_headers):
        response = client.get("/users/", headers=auth_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_user_by_id(self, client, test_user, auth_headers):
        response = client.get(f"/users/{test_user.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_user.id

    def test_update_user(self, client, test_user, auth_headers):
        update_data = {
            "first_name": "Updated",
            "last_name": "Name"
        }
        
        response = client.put(f"/users/{test_user.id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["first_name"] == "Updated"
        assert data["last_name"] == "Name"

    def test_update_user_unauthorized(self, client, test_user):
        update_data = {"first_name": "Updated"}
        
        response = client.put(f"/users/{test_user.id}", json=update_data)
        
        # HTTPBearer returns 403 when no auth header provided
        assert response.status_code == status.HTTP_403_FORBIDDEN
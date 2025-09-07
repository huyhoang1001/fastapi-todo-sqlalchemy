import pytest
from fastapi import status

class TestAuth:
    def test_login_success(self, client, test_user):
        response = client.post(
            "/auth/login",
            data={"username": test_user.email, "password": "testpass123"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_email(self, client):
        response = client.post(
            "/auth/login",
            data={"username": "wrong@example.com", "password": "testpass123"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_wrong_password(self, client, test_user):
        response = client.post(
            "/auth/login",
            data={"username": test_user.email, "password": "wrongpassword"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_inactive_user(self, client, db_session):
        from app.models.user import User
        from app.core.security import get_password_hash
        
        inactive_user = User(
            email="inactive@example.com",
            username="inactive",
            first_name="Inactive",
            last_name="User",
            hashed_password=get_password_hash("testpass123"),
            is_active=False
        )
        db_session.add(inactive_user)
        db_session.commit()
        
        response = client.post(
            "/auth/login",
            data={"username": inactive_user.email, "password": "testpass123"}
        )
        
        # Login succeeds but user is inactive - checked at endpoint level
        assert response.status_code == status.HTTP_200_OK
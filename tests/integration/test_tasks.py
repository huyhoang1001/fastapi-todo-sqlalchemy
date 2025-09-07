import pytest
from fastapi import status

class TestTasks:
    def test_create_task(self, client, auth_headers):
        task_data = {
            "summary": "New Task",
            "description": "Task description",
            "status": "pending",
            "priority": "high"
        }
        
        response = client.post("/tasks/", json=task_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["summary"] == task_data["summary"]
        assert data["description"] == task_data["description"]

    def test_create_task_unauthorized(self, client):
        task_data = {
            "summary": "New Task",
            "description": "Task description"
        }
        
        response = client.post("/tasks/", json=task_data)
        
        # HTTPBearer returns 403 when no auth header provided
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_user_tasks(self, client, test_task, auth_headers):
        response = client.get("/tasks/", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(task["id"] == test_task.id for task in data)

    def test_get_task_by_id(self, client, test_task, auth_headers):
        response = client.get(f"/tasks/{test_task.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_task.id
        assert data["summary"] == test_task.summary

    def test_get_task_not_found(self, client, auth_headers):
        response = client.get("/tasks/99999", headers=auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_task(self, client, test_task, auth_headers):
        update_data = {
            "summary": "Updated Task",
            "status": "completed"
        }
        
        response = client.put(f"/tasks/{test_task.id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["summary"] == "Updated Task"
        assert data["status"] == "completed"

    def test_update_task_not_owner(self, client, test_task, db_session):
        # Create another user
        from app.models.user import User
        from app.core.security import get_password_hash
        
        other_user = User(
            email="other@example.com",
            username="otheruser",
            first_name="Other",
            last_name="User",
            hashed_password=get_password_hash("otherpass123"),
            is_active=True
        )
        db_session.add(other_user)
        db_session.commit()
        
        # Login as other user
        login_response = client.post(
            "/auth/login",
            data={"username": other_user.email, "password": "otherpass123"}
        )
        other_headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        
        update_data = {"summary": "Hacked Task"}
        response = client.put(f"/tasks/{test_task.id}", json=update_data, headers=other_headers)
        
        # API returns 400 for permission errors, not 404
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_task(self, client, test_task, auth_headers):
        response = client.delete(f"/tasks/{test_task.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify task is deleted
        get_response = client.get(f"/tasks/{test_task.id}", headers=auth_headers)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task_unauthorized(self, client, test_task):
        response = client.delete(f"/tasks/{test_task.id}")
        
        # HTTPBearer returns 403 when no auth header provided
        assert response.status_code == status.HTTP_403_FORBIDDEN
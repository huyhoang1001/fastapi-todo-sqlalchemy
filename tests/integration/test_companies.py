import pytest
from fastapi import status

class TestCompanies:
    def test_create_company_admin(self, client, admin_headers):
        company_data = {
            "name": "New Company",
            "description": "Company description",
            "mode": "active",
            "rating": 4.5
        }
        
        response = client.post("/companies/", json=company_data, headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == company_data["name"]
        assert data["rating"] == company_data["rating"]

    def test_create_company_non_admin(self, client, auth_headers):
        company_data = {
            "name": "New Company",
            "description": "Company description"
        }
        
        response = client.post("/companies/", json=company_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_company_unauthorized(self, client):
        company_data = {
            "name": "New Company",
            "description": "Company description"
        }
        
        response = client.post("/companies/", json=company_data)
        
        # HTTPBearer returns 403 when no auth header provided
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_companies(self, client, test_company, auth_headers):
        response = client.get("/companies/", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_company_by_id(self, client, test_company, auth_headers):
        response = client.get(f"/companies/{test_company.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_company.id
        assert data["name"] == test_company.name

    def test_get_company_not_found(self, client, auth_headers):
        response = client.get("/companies/99999", headers=auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_company_admin(self, client, test_company, admin_headers):
        update_data = {
            "name": "Updated Company",
            "rating": 5.0
        }
        
        response = client.put(f"/companies/{test_company.id}", json=update_data, headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Company"
        assert data["rating"] == 5.0

    def test_update_company_non_admin(self, client, test_company, auth_headers):
        update_data = {"name": "Updated Company"}
        
        response = client.put(f"/companies/{test_company.id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_company_admin(self, client, test_company, admin_headers):
        response = client.delete(f"/companies/{test_company.id}", headers=admin_headers)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify company is deleted
        get_response = client.get(f"/companies/{test_company.id}", headers=admin_headers)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_company_non_admin(self, client, test_company, auth_headers):
        response = client.delete(f"/companies/{test_company.id}", headers=auth_headers)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_company_unauthorized(self, client, test_company):
        response = client.delete(f"/companies/{test_company.id}")
        
        # HTTPBearer returns 403 when no auth header provided
        assert response.status_code == status.HTTP_403_FORBIDDEN
import pytest
from fastapi import status

class TestMain:
    def test_root_endpoint(self, client):
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert data["message"] == "Welcome to Todo API"

    def test_openapi_docs(self, client):
        response = client.get("/docs")
        
        assert response.status_code == status.HTTP_200_OK

    def test_openapi_json(self, client):
        response = client.get("/openapi.json")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "Todo API"
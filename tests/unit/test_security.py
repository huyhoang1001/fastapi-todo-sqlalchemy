import pytest
from datetime import timedelta
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token
)

class TestSecurity:
    def test_password_hashing(self):
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False

    def test_create_access_token(self):
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)

    def test_create_access_token_with_expiry(self):
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta)
        
        assert token is not None
        payload = verify_token(token)
        assert payload["sub"] == "testuser"

    def test_verify_token_valid(self):
        data = {"sub": "testuser"}
        token = create_access_token(data)
        payload = verify_token(token)
        
        assert payload is not None
        assert payload["sub"] == "testuser"

    def test_verify_token_invalid(self):
        invalid_token = "invalid.token.here"
        payload = verify_token(invalid_token)
        
        assert payload is None
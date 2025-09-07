# Test Suite for FastAPI Todo Application

This directory contains comprehensive unit and integration tests for the FastAPI Todo application.

## Test Structure

```
tests/
├── conftest.py              # Test configuration and fixtures
├── unit/                    # Unit tests
│   ├── test_security.py     # Security functions tests
│   ├── test_models.py       # Database model tests
│   └── test_crud.py         # CRUD operation tests
└── integration/             # Integration tests
    ├── test_main.py         # Main app endpoint tests
    ├── test_auth.py         # Authentication endpoint tests
    ├── test_users.py        # User endpoint tests
    ├── test_tasks.py        # Task endpoint tests
    └── test_companies.py    # Company endpoint tests
```

## Running Tests

### Install Test Dependencies
```bash
pip install -r requirements-test.txt
```

### Run All Tests
```bash
pytest tests/
```

### Run Unit Tests Only
```bash
pytest tests/unit/
```

### Run Integration Tests Only
```bash
pytest tests/integration/
```

### Run with Verbose Output
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/unit/test_security.py -v
```

### Run Tests with Coverage
```bash
pip install pytest-cov
pytest tests/ --cov=app --cov-report=html
```

## Test Features

### Unit Tests
- **Security Functions**: Password hashing, JWT token creation/verification
- **Database Models**: Model creation, relationships, defaults
- **CRUD Operations**: Create, read, update, delete operations for all entities

### Integration Tests
- **Authentication**: Login success/failure, token validation
- **User Management**: User creation, retrieval, updates, admin permissions
- **Task Management**: CRUD operations, ownership validation
- **Company Management**: Admin-only operations, access control
- **API Endpoints**: Status codes, response validation, error handling

### Test Fixtures
- `db_session`: Clean database session for each test
- `client`: FastAPI test client
- `test_user`: Regular user for testing
- `test_admin`: Admin user for testing
- `test_company`: Sample company data
- `test_task`: Sample task data
- `auth_headers`: Authentication headers for regular user
- `admin_headers`: Authentication headers for admin user

## Test Database

Tests use SQLite in-memory database for isolation and speed. Each test gets a fresh database instance.

## Running the Test Suite Script

Use the provided test runner:
```bash
python run_tests.py
```

This will:
1. Install test dependencies
2. Run unit tests
3. Run integration tests
4. Provide a summary of results
import pytest
from app.models.user import User
from app.models.company import Company
from app.models.task import Task

class TestUserModel:
    def test_create_user(self, db_session):
        user = User(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            hashed_password="hashedpass",
            is_active=True,
            is_admin=False
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.is_admin is False

    def test_user_relationships(self, db_session):
        user = User(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            hashed_password="hashedpass"
        )
        db_session.add(user)
        db_session.commit()
        
        task = Task(
            summary="Test Task",
            description="Test Description",
            user_id=user.id
        )
        db_session.add(task)
        db_session.commit()
        
        assert len(user.tasks) == 1
        assert user.tasks[0].summary == "Test Task"

class TestCompanyModel:
    def test_create_company(self, db_session):
        company = Company(
            name="Test Company",
            description="Test Description",
            mode="active",
            rating=4.5
        )
        db_session.add(company)
        db_session.commit()
        
        assert company.id is not None
        assert company.name == "Test Company"
        assert company.rating == 4.5

class TestTaskModel:
    def test_create_task(self, db_session, test_user):
        task = Task(
            summary="Test Task",
            description="Test Description",
            status="pending",
            priority="high",
            user_id=test_user.id
        )
        db_session.add(task)
        db_session.commit()
        
        assert task.id is not None
        assert task.summary == "Test Task"
        assert task.status == "pending"
        assert task.user_id == test_user.id

    def test_task_defaults(self, db_session, test_user):
        task = Task(
            summary="Test Task",
            user_id=test_user.id
        )
        db_session.add(task)
        db_session.commit()
        
        assert task.status == "pending"
        assert task.priority == "medium"
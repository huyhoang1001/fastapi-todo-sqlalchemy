import pytest
from app.crud import user, task, company
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.company import CompanyCreate, CompanyUpdate

class TestCRUDUser:
    def test_create_user(self, db_session):
        user_in = UserCreate(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            password="testpass123",
            is_active=True
        )
        created_user = user.create(db_session, obj_in=user_in)
        
        assert created_user.email == user_in.email
        assert created_user.username == user_in.username
        assert created_user.is_active is True
        assert hasattr(created_user, "hashed_password")

    def test_get_user_by_email(self, db_session, test_user):
        found_user = user.get_by_email(db_session, email=test_user.email)
        
        assert found_user is not None
        assert found_user.email == test_user.email

    def test_get_user_by_username(self, db_session, test_user):
        found_user = user.get_by_username(db_session, username=test_user.username)
        
        assert found_user is not None
        assert found_user.username == test_user.username

    def test_authenticate_user(self, db_session, test_user):
        authenticated = user.authenticate(
            db_session, email=test_user.email, password="testpass123"
        )
        
        assert authenticated is not None
        assert authenticated.email == test_user.email

    def test_authenticate_user_wrong_password(self, db_session, test_user):
        authenticated = user.authenticate(
            db_session, email=test_user.email, password="wrongpassword"
        )
        
        assert authenticated is None

    def test_is_active(self, test_user):
        assert user.is_active(test_user) is True

    def test_is_admin(self, test_admin):
        assert user.is_admin(test_admin) is True

class TestCRUDTask:
    def test_create_task_with_owner(self, db_session, test_user):
        task_in = TaskCreate(
            summary="Test Task",
            description="Test Description",
            status="pending",
            priority="high"
        )
        created_task = task.create_with_owner(
            db_session, obj_in=task_in, owner_id=test_user.id
        )
        
        assert created_task.summary == task_in.summary
        assert created_task.user_id == test_user.id

    def test_get_tasks_by_owner(self, db_session, test_user, test_task):
        tasks = task.get_multi_by_owner(db_session, owner_id=test_user.id)
        
        assert len(tasks) == 1
        assert tasks[0].id == test_task.id

    def test_update_task(self, db_session, test_task):
        task_update = TaskUpdate(summary="Updated Task", status="completed")
        updated_task = task.update(db_session, db_obj=test_task, obj_in=task_update)
        
        assert updated_task.summary == "Updated Task"
        assert updated_task.status == "completed"

class TestCRUDCompany:
    def test_create_company(self, db_session):
        company_in = CompanyCreate(
            name="Test Company",
            description="Test Description",
            mode="active",
            rating=4.5
        )
        created_company = company.create(db_session, obj_in=company_in)
        
        assert created_company.name == company_in.name
        assert created_company.rating == company_in.rating

    def test_get_company(self, db_session, test_company):
        found_company = company.get(db_session, id=test_company.id)
        
        assert found_company is not None
        assert found_company.name == test_company.name

    def test_update_company(self, db_session, test_company):
        company_update = CompanyUpdate(name="Updated Company", rating=5.0)
        updated_company = company.update(
            db_session, db_obj=test_company, obj_in=company_update
        )
        
        assert updated_company.name == "Updated Company"
        assert updated_company.rating == 5.0

    def test_delete_company(self, db_session, test_company):
        deleted_company = company.remove(db_session, id=test_company.id)
        
        assert deleted_company.id == test_company.id
        
        # Verify it's deleted
        found_company = company.get(db_session, id=test_company.id)
        assert found_company is None
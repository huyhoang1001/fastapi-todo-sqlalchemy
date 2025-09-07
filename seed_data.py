import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.security import get_password_hash
from app.models.user import User
from app.models.company import Company
from app.models.task import Task
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:admin@localhost/todoapp")

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_database():
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Task).delete()
        db.query(User).delete()
        db.query(Company).delete()
        db.commit()
        
        # Create users
        users_data = [
            {"email": "admin@example.com", "username": "admin", "first_name": "Admin", "last_name": "User", "password": "admin123", "is_admin": True},
            {"email": "john@example.com", "username": "john", "first_name": "John", "last_name": "Doe", "password": "password123", "is_admin": False},
            {"email": "jane@example.com", "username": "jane", "first_name": "Jane", "last_name": "Smith", "password": "password123", "is_admin": False},
            {"email": "bob@example.com", "username": "bob", "first_name": "Bob", "last_name": "Johnson", "password": "password123", "is_admin": False},
            {"email": "alice@example.com", "username": "alice", "first_name": "Alice", "last_name": "Brown", "password": "password123", "is_admin": False},
        ]
        
        users = []
        for user_data in users_data:
            user_obj = User(
                email=user_data["email"],
                username=user_data["username"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                hashed_password=get_password_hash(user_data["password"]),
                is_active=True,
                is_admin=user_data["is_admin"]
            )
            db.add(user_obj)
            users.append(user_obj)
        
        db.commit()
        for user_obj in users:
            db.refresh(user_obj)
        
        # Create companies
        companies_data = [
            {"name": "Tech Corp", "description": "Technology company", "mode": "active", "rating": 4.5},
            {"name": "StartupXYZ", "description": "Innovative startup", "mode": "active", "rating": 4.2},
            {"name": "Enterprise Ltd", "description": "Large enterprise", "mode": "active", "rating": 4.8},
            {"name": "Creative Agency", "description": "Design and marketing", "mode": "active", "rating": 4.3},
            {"name": "Consulting Group", "description": "Business consulting", "mode": "active", "rating": 4.6},
        ]
        
        companies = []
        for company_data in companies_data:
            company_obj = Company(**company_data)
            db.add(company_obj)
            companies.append(company_obj)
        
        db.commit()
        for company_obj in companies:
            db.refresh(company_obj)
        
        # Create tasks
        tasks_data = [
            {"summary": "Setup development environment", "description": "Install and configure development tools", "status": "completed", "priority": "high", "user_id": users[1].id},
            {"summary": "Design database schema", "description": "Create ERD and database design", "status": "completed", "priority": "high", "user_id": users[1].id},
            {"summary": "Implement user authentication", "description": "Add JWT-based authentication", "status": "in_progress", "priority": "high", "user_id": users[1].id},
            {"summary": "Create API documentation", "description": "Write comprehensive API docs", "status": "pending", "priority": "medium", "user_id": users[1].id},
            {"summary": "Write unit tests", "description": "Add test coverage for all modules", "status": "pending", "priority": "medium", "user_id": users[2].id},
            {"summary": "Setup CI/CD pipeline", "description": "Configure automated deployment", "status": "pending", "priority": "low", "user_id": users[2].id},
            {"summary": "Code review", "description": "Review pull requests", "status": "in_progress", "priority": "medium", "user_id": users[2].id},
            {"summary": "Bug fixes", "description": "Fix reported issues", "status": "in_progress", "priority": "high", "user_id": users[3].id},
            {"summary": "Performance optimization", "description": "Optimize database queries", "status": "pending", "priority": "medium", "user_id": users[3].id},
            {"summary": "Security audit", "description": "Conduct security assessment", "status": "pending", "priority": "high", "user_id": users[4].id},
            {"summary": "User interface design", "description": "Create mockups and wireframes", "status": "completed", "priority": "medium", "user_id": users[4].id},
            {"summary": "Mobile app development", "description": "Build mobile application", "status": "pending", "priority": "low", "user_id": users[4].id},
        ]
        
        for task_data in tasks_data:
            task_obj = Task(**task_data)
            db.add(task_obj)
        
        db.commit()
        
        print("Database seeded successfully!")
        print(f"Created {len(users)} users")
        print(f"Created {len(companies)} companies")
        print(f"Created {len(tasks_data)} tasks")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.core.security import get_password_hash
from app.models.user import User
from app.models import user, company, task

# Create tables
user.Base.metadata.create_all(bind=engine)

def create_admin_user():
    db = SessionLocal()
    
    # Check if admin already exists
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if admin:
        print("Admin user already exists")
        return
    
    # Create admin user
    admin_user = User(
        email="admin@example.com",
        username="admin",
        first_name="Admin",
        last_name="User",
        hashed_password=get_password_hash("admin123"),
        is_active=True,
        is_admin=True
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    print("Admin user created successfully!")
    print("Email: admin@example.com")
    print("Password: admin123")
    
    db.close()

if __name__ == "__main__":
    create_admin_user()
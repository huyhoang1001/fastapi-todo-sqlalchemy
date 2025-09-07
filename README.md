# FastAPI Todo Application

A complete Todo application built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- User authentication with JWT tokens
- Role-based access control (admin/user)
- CRUD operations for Users, Companies, and Tasks
- Database migrations with Alembic
- Data validation with Pydantic
- PostgreSQL database

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup PostgreSQL database:**
   - Create a database named `todoapp`
   - Update database credentials in `.env` file

3. **Run migrations:**
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

## API Endpoints

### Authentication
- `POST /auth/login` - Login with email/password

### Users
- `POST /users/` - Create user
- `GET /users/` - List users (admin only)
- `GET /users/me` - Get current user
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user

### Companies
- `POST /companies/` - Create company (admin only)
- `GET /companies/` - List companies
- `GET /companies/{company_id}` - Get company
- `PUT /companies/{company_id}` - Update company (admin only)
- `DELETE /companies/{company_id}` - Delete company (admin only)

### Tasks
- `POST /tasks/` - Create task
- `GET /tasks/` - List user's tasks
- `GET /tasks/{task_id}` - Get task
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task

## Database Schema

### Users
- id, email, username, first_name, last_name, hashed_password, is_active, is_admin

### Companies
- id, name, description, mode, rating

### Tasks
- id, summary, description, status, priority, user_id

## Environment Variables

Create a `.env` file with:
```
DATABASE_URL=postgresql://user:password@localhost/todoapp
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
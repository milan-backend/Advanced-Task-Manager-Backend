# Task Management Backend (FastAPI)

A production-style backend API built using **FastAPI** that supports authentication, authorization, project collaboration, task management, pagination, and secure token handling.

This project focuses on **real backend fundamentals**, not just CRUD — including JWT authentication, refresh tokens, role-based access logic, pagination, and clean API design.

---

##  Features

###  Authentication & Security
- User signup & login
- JWT access token authentication
- Refresh token mechanism for better user experience
- Password hashing (no plain-text passwords)
- Protected routes using HTTP Bearer tokens
- Token revocation support (logout)

---

###  Authorization
- Project-based access control
- Only project owners can:
  - Add/remove members
  - Manage project settings
- Members can collaborate within allowed projects
- Strict backend-side validation (no client trust)

---

###  Project Management
- Create projects
- List user-owned projects
- Add members to projects
- Many-to-many relationship between users and projects

---

###  Task Management
- Create tasks inside projects
- Update tasks using PATCH (partial updates)
- Assign tasks to users
- Track task status (`TODO`, `IN_PROGRESS`, `DONE`)
- Filter and paginate tasks
- Secure access to tasks based on project membership

---

##  Database & Migrations
- PostgreSQL is used as the primary database
- Database schema changes are handled using **Alembic migrations**
- Proper foreign keys, constraints, and relationships are enforced
- Designed with production-ready relational modeling

---

##  Testing
- All endpoints were manually tested using:
  - Swagger UI
  - Postman
- Authentication, authorization, and edge cases were verified manually

---

##  Deployment
- Backend can be deployed on platforms like **Render**
- Environment variables are used for secrets and configuration
- PostgreSQL is recommended for production deployments

---

##  Tech Stack
- **FastAPI**
- **SQLModel**
- **PostgreSQL**
- **JWT (python-jose)**
- **Passlib (bcrypt)**
- **Alembic**
- **Python-dotenv**

---

##  Learning Outcomes

Through this project, I learned:
- How JWT authentication works (access vs refresh tokens)
- Secure backend authorization patterns
- Proper API design (PUT vs PATCH)
- Pagination and filtering
- One-to-many & many-to-many relationships
- Database migrations with Alembic
- PostgreSQL vs SQLite limitations
- Real-world backend debugging and design decisions

---

##  Future Improvements
- Add automated tests (pytest)
- Add role-based permissions (admin/user)
- Add async database support
- Improve deployment using Docker
- Add rate limiting and monitoring

---

##  Environment Variables

Create a `.env` file using `.env.example` as reference and provide real values:

```env
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/advanced_task_manager
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7


## ▶️ Running Locally

```bash
# Clone the repository
git clone https://github.com/milan-backend/Advanced-Task-Manager-Backend.git
cd Task-Manager-Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the FastAPI server
uvicorn main:app --reload

Once the server is running, open:
Swagger UI: http://127.0.0.1:8000/docs
OpenAPI JSON: http://127.0.0.1:8000/openapi.json
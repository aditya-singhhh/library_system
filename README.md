Library System Project - README

1. How to Run the Project

Prerequisites

Python Installation:

Ensure Python 3.8 or higher is installed on your system.

Package Manager:

Install pip for managing Python dependencies.

Database:

Set up a PostgreSQL database (or any other supported SQLAlchemy database).

Steps to Run

Clone the Repository:

git clone <repository-url>
cd LIBRARY_SYSTEM

Set Up Virtual Environment:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install Dependencies:

pip install -r requirements.txt

Set Up Environment Configuration:

Create a .env file or modify the instance/config.py file.

Provide the following configurations:

SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=your-database-uri

Initialize the Database:

Use Flask-Migrate for database migrations (if set up):

flask db init
flask db migrate
flask db upgrade

Alternatively, create tables directly:

from app.models import db
db.create_all()

Run the Application:

flask run

The application will be available at http://127.0.0.1:5000/ by default.

2. Design Choices Made

Modularity

The project is structured into blueprints (auth, books, members) to achieve modularity and separation of concerns. Each module handles specific functionalities:

auth.py: Manages user authentication and authorization.

books.py: Manages book-related operations.

members.py: Manages member-related operations.

Security

Token-Based Authentication:

JWTs are used for stateless authentication.

Tokens are stored in secure cookies (HttpOnly, Secure, SameSite attributes).

Role-Based Access Control (RBAC):

Decorators (login_required) enforce role-specific access.

Password Hashing:

Passwords are hashed using pbkdf2:sha256 for secure storage.

Scalability

Pagination:

All list-based endpoints (e.g., books, members) implement pagination to handle large datasets efficiently.

Database Abstraction:

SQLAlchemy is used for ORM, enabling easy migration to other databases if required.

Validation

Input validation ensures data integrity:

Required fields are checked in API endpoints.

Role values are validated against a predefined set.

Configuration Management

Sensitive data like the SECRET_KEY and database credentials are managed through environment variables.

3. Assumptions and Limitations

Assumptions

Roles:

Users have two roles: admin and user.

admin has full access, while user has limited access.

Book Availability:

The available field indicates whether a book can be borrowed but does not track actual borrowing.

Limitations

Borrowing System:

The current implementation does not track book borrowing or returns.

Search Functionality:

The search feature supports only basic filtering by title and author.

Email Validation:

No advanced email validation or verification mechanism is implemented.

Scalability:

While the application supports pagination, it has not been optimized for high concurrency or very large datasets.

For further assistance or inquiries, feel free to reach out!


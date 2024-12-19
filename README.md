# Library System Project - README

## 1. How to Run the Project

### Prerequisites
1. **Python Installation**:
   - Ensure Python 3.8 or higher is installed on your system.
2. **Package Manager**:
   - Install `pip` to manage Python dependencies.
3. **Database**:
   - Set up SQLAlchemy database.
     
### Steps to Run

1. **Clone the Repository**:
````
git clone <repository-url>
cd library_system
````
2. **Set Up Virtual Environment**:
````
python -m venv venv
venv\Scripts\activate
````
3. **Install Dependencies:**
````
pip install -r requirements.txt
````
4. **Run the Application:**
````
python run.py
````
The application will be available at http://127.0.0.1:5000/ by default.

## 2. Design Choices Made

### Modularity

The project is structured into blueprints (auth, books, members) to achieve modularity and separation of concerns. Each module handles specific functionalities:

**auth.py**: Manages user authentication and authorization.

**books.py**: Manages book-related operations.

**members.py**: Manages member-related operations.

### Security

**Token-Based Authentication**: JWTs are used for stateless authentication. Tokens are stored in secure cookies (HttpOnly, Secure, SameSite attributes).

**Role-Based Access Control (RBAC)**: Decorators (login_required) enforce role-specific access.

**Password Hashing**: Passwords are hashed using pbkdf2:sha256 for secure storage.

### Scalability

**Pagination**: All list-based endpoints (e.g., books, members) implement pagination to handle large datasets efficiently.

**Database Abstraction**: SQLAlchemy is used for ORM, enabling easy migration to other databases if required.

**Validation**: Input validation ensures data integrity. Required fields are checked in API endpoints. Role values are validated against a predefined set.


### 3. Assumptions and Limitations

## Assumptions

**Roles**: Users have two roles i.e. admin and user. admin has full access, while the user has limited access.

**Book Availability**: The available field indicates whether a book can be borrowed but does not track actual borrowing.

### Limitations

**Search Functionality**: The search feature supports only basic filtering by title and author.

**Email Validation**: No advanced email validation or verification mechanism is implemented.

Scalability:

While the application supports pagination, it has not been optimized for high concurrency or very large datasets.

For further assistance or inquiries, feel free to reach out!


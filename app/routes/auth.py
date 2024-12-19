from flask import Blueprint, request, jsonify, current_app, make_response
from app.models import db, Member
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Get the secret key dynamically from current_app
def generate_token(member):
    secret_key = current_app.config.get('SECRET_KEY', 'your-secret-key')
    payload = {
        'id': member.id,
        'role': member.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def login_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Get the token from cookies
            token = request.cookies.get('auth_token')
            if not token:
                return jsonify({'error': 'Token is missing'}), 401

            try:
                # Decode the token using the secret key
                decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                # Check if the role matches or is 'any'
                if decoded['role'] != role and role != 'any':
                    return jsonify({'error': 'Unauthorized access'}), 403
                # Store the decoded user data in request
                request.user = decoded
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401

            return f(*args, **kwargs)
        return wrapper
    return decorator


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']
    member = Member.query.filter_by(email=email).first()

    if not member or not check_password_hash(member.password, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = generate_token(member)
    response = make_response(jsonify({'message': 'Login successful', 'role': member.role}))
    response.set_cookie(
        'auth_token',
        token,
        httponly=True,
        secure=True,  # Use True only in production with HTTPS
        samesite='Strict',
        max_age=3600  # 1 hour
    )
    return response, 200

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json

    # Validate required fields
    if not data or 'name' not in data or 'email' not in data or 'password' not in data or 'role' not in data:
        return jsonify({'error': 'Name, email, password, and role are required'}), 400

    # Validate role value (Case insensitive)
    valid_roles = ['user', 'admin']  # Define valid roles
    role = data['role'].strip().lower()
    if role not in valid_roles:
        return jsonify({'error': f'Invalid role. Allowed roles are: {", ".join(valid_roles)}'}), 400

    # Check if email is already registered
    if Member.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email is already registered'}), 409

    # Hash the password
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    # Create and save the new member
    new_member = Member(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        role=role
    )
    db.session.add(new_member)
    db.session.commit()

    return jsonify({'message': 'Signup successful'}), 201


@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'message': 'Logout successful'}))
    response.delete_cookie('auth_token')
    return response, 200

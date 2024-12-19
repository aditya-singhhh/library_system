from flask import Blueprint, request, jsonify, current_app
from app.models import db, Book
from app.routes.auth import login_required
import jwt

bp = Blueprint('books', __name__, url_prefix='/books')

# Fetch all books with pagination
@bp.route('/viewall', methods=['GET'])
@login_required(role='any')  # Accessible to all logged-in users
def view_all_books():
    # Get pagination parameters from query string, with defaults
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    books = Book.query.paginate(page, per_page, False)
    
    # Create the response with pagination data
    return jsonify({
        'total': books.total,
        'pages': books.pages,
        'current_page': books.page,
        'per_page': books.per_page,
        'books': [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'available': book.available
        } for book in books.items]
    })

# Create a new book
@bp.route('/create', methods=['POST'])
@login_required(role='admin')  # Accessible to admins only
def create_book():
    data = request.json
    if 'title' not in data or 'author' not in data:
        return jsonify({'error': 'Title and author are required'}), 400
    new_book = Book(
        title=data['title'],
        author=data['author'],
        genre=data.get('genre'),
        available=data.get('available', True)
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'}), 201

# View a specific book by ID
@bp.route('/view/<int:id>', methods=['GET'])
@login_required(role='any')  # Accessible to all logged-in users
def view_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'genre': book.genre,
        'available': book.available
    })

# Update a specific book by ID
@bp.route('/update/<int:id>', methods=['PUT'])
@login_required(role='admin')  # Accessible to admins only
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.json
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.genre = data.get('genre', book.genre)
    book.available = data.get('available', book.available)
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

# Delete a specific book by ID
@bp.route('/delete/<int:id>', methods=['DELETE'])
@login_required(role='admin')  # Accessible to admins only
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

# Search for books by title or author with pagination
@bp.route('/search', methods=['GET'])
@login_required(role='any')  # Accessible to all logged-in users
def search_books():
    title = request.args.get('title')
    author = request.args.get('author')
    
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = Book.query
    
    # Search by title if provided
    if title:
        query = query.filter(Book.title.ilike(f'%{title}%'))
    
    # Search by author if provided
    if author:
        query = query.filter(Book.author.ilike(f'%{author}%'))
    
    books = query.paginate(page, per_page, False)
    
    # Create the response with pagination data
    return jsonify({
        'total': books.total,
        'pages': books.pages,
        'current_page': books.page,
        'per_page': books.per_page,
        'books': [{
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'available': book.available
        } for book in books.items]
    })

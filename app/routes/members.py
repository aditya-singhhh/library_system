from flask import Blueprint, request, jsonify
from app.models import db, Member
from app.routes.auth import login_required  # Import the login_required decorator

bp = Blueprint('members', __name__, url_prefix='/members')

# Fetch all members (admin only)
@bp.route('/viewall', methods=['GET'])
@login_required(role='admin')  # Ensures only admins can access this route
def view_all_members():
    members = Member.query.all()
    return jsonify([{
        'id': member.id,
        'name': member.name,
        'email': member.email
    } for member in members])

# Create a new member (admin only)
@bp.route('/create', methods=['POST'])
@login_required(role='admin')  # Ensures only admins can access this route
def create_member():
    data = request.json
    if 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email are required'}), 400
    new_member = Member(
        name=data['name'],
        email=data['email']
    )
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'Member created successfully'}), 201

# View a specific member by ID (admin only)
@bp.route('/view/<int:id>', methods=['GET'])
@login_required(role='admin')  # Ensures only admins can access this route
def view_member(id):
    member = Member.query.get_or_404(id)
    return jsonify({
        'id': member.id,
        'name': member.name,
        'email': member.email
    })

# Update a specific member by ID (admin only)
@bp.route('/update/<int:id>', methods=['PUT'])
@login_required(role='admin')  # Ensures only admins can access this route
def update_member(id):
    member = Member.query.get_or_404(id)
    data = request.json
    member.name = data.get('name', member.name)
    member.email = data.get('email', member.email)
    db.session.commit()
    return jsonify({'message': 'Member updated successfully'})

# Delete a specific member by ID (admin only)
@bp.route('/delete/<int:id>', methods=['DELETE'])
@login_required(role='admin')  # Ensures only admins can access this route
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member deleted successfully'})

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    with app.app_context():
        from app.routes import books, members, auth
        app.register_blueprint(books.bp)
        app.register_blueprint(members.bp)
        app.register_blueprint(auth.auth_bp)

        db.create_all()

    return app

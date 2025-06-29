from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration
    # Use an environment variable for the secret key, or a default for development
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    # Define the database URI. We'll use SQLite for simplicity.
    # It will create a file named 'time_tracker.db' in the instance folder.
    # The instance folder is automatically created by Flask at app.instance_path.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'time_tracker.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass # Already exists

    db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes
        from . import models # Import models to ensure they are known to SQLAlchemy

        # Create database tables if they don't exist
        # This is okay for development. For production, migrations (e.g. Alembic) are better.
        db.create_all()

    return app

import os
from werkzeug.security import generate_password_hash
from app import app
from models import db, User, Staff

def init_database():
    """
    Initializes the SQLite database using SQLAlchemy and
    seeds initial users for the application.
    """
    with app.app_context():
        # Get path from app config (Flask-SQLAlchemy default puts it in instance folder)
        DB_PATH = os.path.join(app.instance_path, 'database.db')
        
        # Ensure instance folder exists
        os.makedirs(app.instance_path, exist_ok=True)
        
        if os.path.exists(DB_PATH):
            print(f"Removing existing database at {DB_PATH} to start fresh...")
            os.remove(DB_PATH)
        
        print("Initializing database...")
        
        # Create all tables defined in models.py
        db.create_all()
        print("Successfully created tables via SQLAlchemy.")
        
        # Seed the initial Admin user
        print("Seeding initial Admin user...")
        admin = User( # type: ignore
            name="System Admin",
            email="admin@trek.com",
            password=generate_password_hash("admin123"),
            role="Admin",
            status="Active"
        )
        db.session.add(admin)

        # Seed the initial Staff user
        print("Seeding initial Staff user...")
        staff = Staff( # type: ignore
            name="Trek Guide",
            email="staff@trek.com",
            password=generate_password_hash("staff123"),
            contact_details="123-456-7890",
            status="Approved"
        )
        db.session.add(staff)

        # Seed the initial User
        print("Seeding initial User...")
        user = User( # type: ignore
            name="Trekker One",
            email="user@trek.com",
            password=generate_password_hash("user123"),
            role="User",
            status="Active"
        )
        db.session.add(user)
        
        db.session.commit()
        
    print("Database initialization complete! You can now log in with:")
    print(f"Admin Email: admin@trek.com, Password: admin123")
    print(f"Staff Email: staff@trek.com, Password: staff123")
    print(f"User Email: user@trek.com, Password: user123")

if __name__ == '__main__':
    init_database()

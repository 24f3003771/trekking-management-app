from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='User') # 'User' or 'Admin'
    status = db.Column(db.String(50), default='Active') # 'Active' or 'Blacklisted'
    
    # Relationship to Bookings
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    contact_details = db.Column(db.Text)
    status = db.Column(db.String(50), default='Pending') # 'Pending', 'Approved', 'Blacklisted'
    
    # Relationship to Treks
    treks = db.relationship('Trek', backref='staff', lazy=True)

class Trek(db.Model):
    __tablename__ = 'treks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='Pending') # 'Pending', 'Approved', 'Open', 'Closed', 'Completed'
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    available_slots = db.Column(db.Integer, nullable=False)
    
    # Relationship to Bookings
    bookings = db.relationship('Booking', backref='trek', lazy=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Confirmed') # 'Confirmed' or 'Cancelled'

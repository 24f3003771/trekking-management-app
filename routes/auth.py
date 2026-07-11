from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from utils import login_required, admin_required, staff_required, user_required
from models import db, User, Staff
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)

        new_user = User(name=name, email=email, password=hashed_password, role='User') # type: ignore
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback() # Rollback if email already exists
            flash('Email already exists.', 'danger')

    return render_template('register.html')

@auth_bp.route('/register/staff', methods=['GET', 'POST'])
def register_staff():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        contact_details = request.form.get('contact_details', '')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return redirect(url_for('auth.register_staff'))

        hashed_password = generate_password_hash(password)

        new_staff = Staff(name=name, email=email, password=hashed_password, contact_details=contact_details) # type: ignore
        
        try:
            db.session.add(new_staff)
            db.session.commit()
            flash('Staff registration successful! Pending approval.', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Email already exists.', 'danger')

    return render_template('register_staff.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            # Check if user is blacklisted
            if user.status == 'Blacklisted':
                flash('Your account has been blacklisted.', 'danger')
                return redirect(url_for('auth.login'))
                
            session['user_id'] = user.id
            session['role'] = user.role
            session['name'] = user.name
            flash('Logged in successfully!', 'success')
            
            # Redirect based on user role
            if user.role == 'Admin':
                return redirect(url_for('admin.admin_dashboard'))
            return redirect(url_for('user.user_dashboard'))
        
        staff = Staff.query.filter_by(email=email).first()
        
        if staff and check_password_hash(staff.password, password):
            if staff.status == 'Blacklisted':
                flash('Your account has been blacklisted.', 'danger')
                return redirect(url_for('auth.login'))
            
            session['user_id'] = staff.id
            session['role'] = 'Staff'
            session['name'] = staff.name
            session['status'] = staff.status # Pending, Approved
            flash('Logged in as Staff!', 'success')
            return redirect(url_for('staff.staff_dashboard'))
            
        flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

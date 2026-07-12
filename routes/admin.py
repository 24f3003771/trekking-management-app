from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils import admin_required
from models import db, User, Staff, Trek, Booking

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role='User').count()
    total_staff = Staff.query.count()
    total_bookings = Booking.query.count()
    
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
        total_treks=total_treks, total_users=total_users, 
        total_staff=total_staff, total_bookings=total_bookings,
        recent_bookings=recent_bookings)

@admin_bp.route('/admin/treks')
@admin_required
def admin_treks():
    search = request.args.get('search', '')
    if search:
        treks = Trek.query.filter(
            (Trek.name.ilike(f'%{search}%')) | 
            (Trek.location.ilike(f'%{search}%')) |
            (Trek.id == (int(search) if search.isdigit() else -1))
        ).all()
    else:
        treks = Trek.query.all()
        
    approved_staff = Staff.query.filter_by(status='Approved').all()
    return render_template('admin/treks.html', treks=treks, approved_staff=approved_staff, search=search)

@admin_bp.route('/admin/trek/create', methods=['POST'])
@admin_required
def admin_trek_create():
    name = request.form.get('name')
    location = request.form.get('location')
    difficulty = request.form.get('difficulty')
    duration = request.form.get('duration')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    available_slots = request.form.get('available_slots')
    assigned_staff_id = request.form.get('assigned_staff_id')
    
    # Handle empty string for dates
    import datetime
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
    
    assigned_staff_id = int(assigned_staff_id) if assigned_staff_id else None

    new_trek = Trek( # type: ignore
        name=name, location=location, difficulty=difficulty,
        duration=duration, start_date=start_date, end_date=end_date,
        available_slots=available_slots, assigned_staff_id=assigned_staff_id,
        status='Pending'
    )
    db.session.add(new_trek)
    db.session.commit()
    flash('Trek created successfully!', 'success')
    return redirect(url_for('admin.admin_treks'))

@admin_bp.route('/admin/trek/edit/<int:trek_id>', methods=['POST'])
@admin_required
def admin_trek_edit(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    trek.name = request.form.get('name')
    trek.location = request.form.get('location')
    trek.difficulty = request.form.get('difficulty')
    trek.duration = request.form.get('duration')
    
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    import datetime
    trek.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
    trek.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
    
    trek.available_slots = request.form.get('available_slots')
    
    assigned_staff_id = request.form.get('assigned_staff_id')
    trek.assigned_staff_id = int(assigned_staff_id) if assigned_staff_id else None
    
    trek.status = request.form.get('status')
    
    db.session.commit()
    flash('Trek updated successfully!', 'success')
    return redirect(url_for('admin.admin_treks'))

@admin_bp.route('/admin/trek/delete/<int:trek_id>', methods=['POST'])
@admin_required
def admin_trek_delete(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    db.session.delete(trek)
    db.session.commit()
    flash('Trek deleted.', 'info')
    return redirect(url_for('admin.admin_treks'))

@admin_bp.route('/admin/users')
@admin_required
def admin_users():
    search = request.args.get('search', '')
    if search:
        users = User.query.filter(
            User.role == 'User',
            ((User.name.ilike(f'%{search}%')) | 
             (User.email.ilike(f'%{search}%')) |
             (User.id == (int(search) if search.isdigit() else -1)))
        ).all()
    else:
        users = User.query.filter_by(role='User').all()
    return render_template('admin/users.html', users=users, search=search)

@admin_bp.route('/admin/user/status/<int:user_id>', methods=['POST'])
@admin_required
def admin_user_status(user_id):
    user = User.query.get_or_404(user_id)
    new_status = request.form.get('status')
    user.status = new_status
    db.session.commit()
    flash(f"User status updated to {new_status}.", 'success')
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/admin/user/delete/<int:user_id>', methods=['POST'])
@admin_required
def admin_user_delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted.', 'info')
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/admin/staff')
@admin_required
def admin_staff():
    search = request.args.get('search', '')
    if search:
        staff = Staff.query.filter(
            (Staff.name.ilike(f'%{search}%')) | 
            (Staff.email.ilike(f'%{search}%')) |
            (Staff.id == (int(search) if search.isdigit() else -1))
        ).all()
    else:
        staff = Staff.query.all()
    return render_template('admin/staff.html', staff=staff, search=search)

@admin_bp.route('/admin/staff/approve/<int:staff_id>', methods=['POST'])
@admin_required
def admin_staff_approve(staff_id):
    staff = Staff.query.get_or_404(staff_id)
    new_status = request.form.get('status')
    staff.status = new_status
    db.session.commit()
    flash(f"Staff status updated to {new_status}.", 'success')
    return redirect(url_for('admin.admin_staff'))

@admin_bp.route('/admin/staff/delete/<int:staff_id>', methods=['POST'])
@admin_required
def admin_staff_delete(staff_id):
    staff = Staff.query.get_or_404(staff_id)
    db.session.delete(staff)
    db.session.commit()
    flash('Staff deleted.', 'info')
    return redirect(url_for('admin.admin_staff'))

@admin_bp.route('/admin/bookings')
@admin_required
def admin_bookings():
    search = request.args.get('search', '')
    if search:
        bookings = Booking.query.join(User).join(Trek).filter(
            (User.name.ilike(f'%{search}%')) | 
            (Trek.name.ilike(f'%{search}%'))
        ).all()
    else:
        bookings = Booking.query.all()
    return render_template('admin/bookings.html', bookings=bookings, search=search)

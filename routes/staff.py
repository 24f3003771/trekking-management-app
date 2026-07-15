from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils import staff_required
from models import db, Trek, Booking, User

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff/dashboard')
@staff_required
def staff_dashboard():
    if session.get('status') != 'Approved':
        flash('Your staff account is pending approval or blacklisted. You cannot access dashboard features.', 'warning')
        return render_template('staff/dashboard.html', treks=[], assigned_treks_count=0, total_participants=0, open_treks_count=0)
        
    treks = Trek.query.filter_by(assigned_staff_id=session['user_id']).all()
    assigned_treks_count = len(treks)
    open_treks_count = sum(1 for t in treks if t.status == 'Open')
    
    total_participants = 0
    for trek in treks:
        bookings = Booking.query.filter_by(trek_id=trek.id, status='Confirmed').all()
        trek.booked_count = len(bookings)
        total_participants += len(bookings)
        
    return render_template('staff/dashboard.html', 
                           treks=treks, 
                           assigned_treks_count=assigned_treks_count,
                           open_treks_count=open_treks_count,
                           total_participants=total_participants)

@staff_bp.route('/staff/manage_trek/<int:trek_id>')
@staff_required
def staff_manage_trek(trek_id):
    if session.get('status') != 'Approved':
        return redirect(url_for('staff.staff_dashboard'))

    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=session['user_id']).first_or_404()
    bookings = Booking.query.filter_by(trek_id=trek.id).all()
    
    return render_template('staff/manage_trek.html', trek=trek, bookings=bookings)

@staff_bp.route('/staff/update_trek/<int:trek_id>', methods=['POST'])
@staff_required
def staff_update_trek(trek_id):
    if session.get('status') != 'Approved':
        return redirect(url_for('staff.staff_dashboard'))
        
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=session['user_id']).first_or_404()
    
    available_slots = request.form.get('available_slots')
    status = request.form.get('status')
    
    if available_slots is not None:
        trek.available_slots = int(available_slots)
    if status:
        trek.status = status
        
    db.session.commit()
    flash('Trek updated successfully.', 'success')
    return redirect(url_for('staff.staff_manage_trek', trek_id=trek_id))


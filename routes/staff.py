from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils import staff_required
from models import db, Trek, Booking, User

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff/dashboard')
@staff_required
def staff_dashboard():
    if session.get('status') != 'Approved':
        flash('Your staff account is pending approval or blacklisted. You cannot access dashboard features.', 'warning')
        return render_template('staff/dashboard.html', treks=[])
        
    treks = Trek.query.filter_by(assigned_staff_id=session['user_id']).all()
    return render_template('staff/dashboard.html', treks=treks)

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

@staff_bp.route('/staff/update_booking/<int:booking_id>', methods=['POST'])
@staff_required
def staff_update_booking(booking_id):
    if session.get('status') != 'Approved':
        return redirect(url_for('staff.staff_dashboard'))
        
    booking = Booking.query.get_or_404(booking_id)
    
    # Ensure this booking belongs to a trek assigned to this staff
    if booking.trek.assigned_staff_id != session['user_id']:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('staff.staff_dashboard'))

    new_status = request.form.get('status')
    
    if booking.status == 'Confirmed' and new_status == 'Cancelled':
        booking.trek.available_slots += 1
    elif booking.status == 'Cancelled' and new_status == 'Confirmed':
        if booking.trek.available_slots > 0:
            booking.trek.available_slots -= 1
        else:
            flash('Cannot confirm booking, no slots available.', 'danger')
            return redirect(url_for('staff.staff_manage_trek', trek_id=booking.trek_id))

    booking.status = new_status
    db.session.commit()
    flash(f'Booking status updated to {new_status}.', 'success')
    return redirect(url_for('staff.staff_manage_trek', trek_id=booking.trek_id))

@staff_bp.route('/staff/complete_trek/<int:trek_id>', methods=['POST'])
@staff_required
def staff_complete_trek(trek_id):
    if session.get('status') != 'Approved':
        return redirect(url_for('staff.staff_dashboard'))
        
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=session['user_id']).first_or_404()
    trek.status = 'Completed'
    db.session.commit()
    flash('Trek marked as completed.', 'success')
    return redirect(url_for('staff.staff_manage_trek', trek_id=trek_id))

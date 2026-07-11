from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from utils import user_required
from models import db, Trek, Booking, User

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/dashboard')
@user_required
def user_dashboard():
    search = request.args.get('search', '')
    if search:
        available_treks = Trek.query.filter(
            Trek.status.in_(['Approved', 'Open']),
            ((Trek.name.ilike(f'%{search}%')) | 
             (Trek.location.ilike(f'%{search}%')))
        ).all()
    else:
        available_treks = Trek.query.filter(Trek.status.in_(['Approved', 'Open'])).all()
        
    return render_template('user/dashboard.html', treks=available_treks, search=search)

@user_bp.route('/trek/<int:trek_id>')
@user_required
def trek_details(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    return render_template('user/trek_details.html', trek=trek)

@user_bp.route('/book/<int:trek_id>', methods=['POST'])
@user_required
def book_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    
    if trek.available_slots > 0 and trek.status in ['Approved', 'Open']:
        # Check if already booked
        existing_booking = Booking.query.filter_by(user_id=session['user_id'], trek_id=trek_id, status='Confirmed').first()
        
        if existing_booking:
            flash('You have already booked this trek.', 'warning')
        else:
            new_booking = Booking(user_id=session['user_id'], trek_id=trek_id) # type: ignore
            trek.available_slots -= 1
            db.session.add(new_booking)
            db.session.commit()
            flash('Trek booked successfully!', 'success')
    else:
        flash('Sorry, no slots available for this trek or it is closed.', 'danger')
        
    return redirect(url_for('user.trek_details', trek_id=trek_id))

@user_bp.route('/user/bookings')
@user_required
def user_bookings():
    bookings = Booking.query.filter_by(user_id=session['user_id']).order_by(Booking.booking_date.desc()).all()
    return render_template('user/bookings.html', bookings=bookings)

@user_bp.route('/user/cancel_booking/<int:booking_id>', methods=['POST'])
@user_required
def cancel_booking(booking_id):
    booking = Booking.query.filter_by(id=booking_id, user_id=session['user_id']).first_or_404()
    
    if booking.status != 'Cancelled':
        booking.status = 'Cancelled'
        booking.trek.available_slots += 1
        db.session.commit()
        flash('Booking cancelled successfully.', 'info')
        
    return redirect(url_for('user.user_bookings'))

@user_bp.route('/user/profile', methods=['GET', 'POST'])
@user_required
def user_profile():
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        password = request.form.get('password')
        
        if password:
            user.password = generate_password_hash(password)
            
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile. Email might already exist.', 'danger')
            
        return redirect(url_for('user.user_profile'))
        
    return render_template('user/profile.html', user=user)

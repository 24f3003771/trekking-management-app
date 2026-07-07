import os
from flask import Flask, render_template, session, redirect, url_for
from models import db
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.staff import staff_bp
from routes.user import user_bp

app = Flask(__name__)
# IMPORTANT: Replace the secret key with a secure environment variable in production
app.secret_key = 'super_secret_key' 

# Set up SQLite database; by default, this creates 'database.db' in the instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(user_bp)

@app.route('/')
def home():
    # If the user is already logged in, redirect them to their respective dashboard
    if 'user_id' in session:
        if session.get('role') == 'Admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif session.get('role') == 'Staff':
            return redirect(url_for('staff.staff_dashboard'))
        elif session.get('role') == 'User':
            return redirect(url_for('user.user_dashboard'))
    return render_template('home.html')

if __name__ == '__main__':
    # Run the application in debug mode for development purposes
    app.run(debug=True, port=5000)

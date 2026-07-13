# Trekking Management Application V2

## Project Overview
This project is built for the MAD-1 college project evaluation. It is a monolithic web application designed to manage trekking operations, staff assignments, and user bookings, adhering to the provided wireframe designs and complete functional requirements. It features a modern, clean UI with glassmorphism effects and responsive design.

## Technology Stack
- **Backend**: Python 3, Flask
- **Database**: Flask-SQLAlchemy (ORM) with SQLite3
- **Frontend**: HTML5, Jinja2 Templating, Bootstrap 5 (CDN), Custom CSS
- **Authentication**: Werkzeug Security (Password Hashing), Flask Session

## Core Features
### 1. Admin Module
- Dedicated Dashboard with statistics (Total Treks, Users, Staff, Bookings) and Recent Bookings ledger.
- Create and manage treks (Duration, Dates, Difficulty, Location, Slots).
- Approve, Blacklist, or Reinstate staff members.
- Assign approved staff to specific treks to open them for booking.
- Manage users (View/Remove) and view the complete system booking ledger.

### 2. Staff Module
- Secure registration capturing contact details and approval workflow.
- Dashboard summarizing assigned treks, open treks, and total participants.
- Manage assigned treks: View participants lists, update available slots, and toggle trek status (Open/Closed/Completed).

### 3. User Module (Trekker)
- Browse available open treks with advanced filtering by Location and Difficulty.
- View detailed trek information before booking.
- Securely book treks (transaction-safe slot decrement to prevent overbooking).
- View personal booking history and cancel upcoming confirmed bookings (automatically incrementing available slots).
- Dedicated Profile page for updating account details.

## Setup Instructions (Local Development)
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment.
4. Install dependencies: `pip install -r requirements.txt`
5. Initialize the database: `python init_db.py`
   - *Note: This drops any existing database, creates the schema using SQLAlchemy models, and seeds the initial Admin, Staff, and User accounts.*
6. Run the application: `python app.py`

## Default Test Credentials
Use these accounts to evaluate different roles in the application immediately after running `init_db.py`:

- **Admin Account**
  - **Email**: admin@trek.com
  - **Password**: admin123

- **Staff Account (Pre-Approved)**
  - **Email**: staff@trek.com
  - **Password**: staff123

- **User Account (Trekker)**
  - **Email**: user@trek.com
  - **Password**: user123

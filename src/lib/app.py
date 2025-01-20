import qrcode
import os
import io
import base64
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import traceback
from datetime import date
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for specific routes and origins
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://localhost:5174"]}}, supports_credentials=True)

# Configure MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/events'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Event(db.Model):
    __tablename__ = 'event'
    event_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    event_name = db.Column(db.String(255))
    event_description = db.Column(db.Text)
    speaker = db.Column(db.String(255))
    location = db.Column(db.String(255))
    event_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    qr_code = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    attendance_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    fullName = db.Column(db.String(256), nullable=False)
    year_and_block = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(256), nullable=False)
    check_in = db.Column(db.DateTime, nullable=True)  
    check_out = db.Column(db.DateTime, nullable=True)  
    status = db.Column(db.String(20), nullable=False)
    

class Participant(db.Model):
    __tablename__ = 'participant'
    student_Id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(256))
    firstName = db.Column(db.String(256))
    lastName = db.Column(db.String(256))
    email = db.Column(db.String(256))
    department = db.Column(db.Text)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class EventRegistration(db.Model):
    __tablename__ = 'event_registration'

    registration_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, nullable=False)  # Foreign key to the Events table
    student_id = db.Column(db.Integer, nullable=False)
    fullname = db.Column(db.Text, nullable=False)
    year_and_block = db.Column(db.String(256), nullable=False)
    department = db.Column(db.String(256), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    registration_status = db.Column(db.String(256), nullable=False, default="registered")


# Routes for Event Management
@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    return jsonify({
        "event_id": event.event_id,
        "event_name": event.event_name,
        "description": event.event_description,
        "location": event.location,
        "event_date": event.event_date.strftime('%Y-%m-%d'),
        "start_time": event.start_time.strftime('%H:%M:%S'),
        "end_time": event.end_time.strftime('%H:%M:%S')
    }), 200

@app.route('/attendance/<int:event_id>', methods=['GET'])
def get_attendance(event_id):
    attendance_records = Attendance.query.filter_by(event_ID=event_id).all()
    if not attendance_records:
        return jsonify({"error": "No attendance records found for this event"}), 404

    participants = []
    for record in attendance_records:
        participant = Participant.query.get(record.participant_ID)
        if participant:
            participants.append({
                "participant_id": participant.student_Id,
                "name": f"{participant.firstName} {participant.lastName}",
                "check_in": record.check_in,
                "status": record.status
            })

    return jsonify({"event_id": event_id, "attendance": participants}), 200

@app.route('/api/events', methods=['GET'])
def get_all_events():
    events = Event.query.all()
    event_list = [
        {
            "event_id": event.event_id,
            "event_name": event.event_name,
            "event_description": event.event_description,
            "speaker": event.speaker,
            "location": event.location,
            "event_date": event.event_date.strftime('%Y-%m-%d'),
            "start_time": event.start_time.strftime('%H:%M:%S'),
            "end_time": event.end_time.strftime('%H:%M:%S')
        }
        for event in events
    ]
    return jsonify(event_list), 200

#Event Creation
@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.json
    required_fields = ['event_name', 'event_description', 'location', 'event_date', 'start_time', 'end_time']

    # Check for required fields
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        event_date = date.fromisoformat(data['event_date'])
        start_time = data['start_time']
        end_time = data['end_time']
    except ValueError as ve:
        return jsonify({"error": f"Invalid date/time format: {ve}"}), 400

    # Create the event in the database
    new_event = Event(
        event_name=data['event_name'],
        event_description=data['event_description'],
        location=data['location'],
        event_date=event_date,
        start_time=start_time,
        end_time=end_time,
        speaker=data.get('speaker', '')
    )

    try:
        db.session.add(new_event)
        db.session.commit()

        return jsonify({"message": "Event created successfully", "event_id": new_event.event_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred during event creation.", "details": str(e)}), 500

#Event Updating
@app.route('/api/events', methods=['PUT'])
def update_event():
    data = request.json
    if not data or 'event_id' not in data:
        return jsonify({"error": "Invalid request data"}), 400

    event = Event.query.get(data['event_id'])
    if not event:
        return jsonify({"error": "Event not found"}), 404

    # Update event details
    event.event_name = data.get('event_name', event.event_name)
    event.event_description = data.get('event_description', event.event_description)
    event.location = data.get('location', event.location)
    event.speaker = data.get('speaker', event.speaker)
    event.event_date = data.get('event_date', event.event_date)
    event.start_time = data.get('start_time', event.start_time)
    event.end_time = data.get('end_time', event.end_time)
    event.qr_code = data.get('qr_code', event.qr_code)

    try:
        db.session.commit()
        return jsonify({"message": "Event updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update event", "details": str(e)}), 500

#Delete Event

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        # Use ORM to fetch and delete the event
        event = Event.query.get(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
            return jsonify({"message": "Event deleted successfully"}), 200
        
        # If event is not found, return 404
        return jsonify({"error": "Event not found"}), 404
    except Exception as e:
        # Log the error and return a 500 response
        return jsonify({"error": "An error occurred while deleting the event", "details": str(e)}), 500

# Routes for Login and Signup
@app.route('/api/user/signup', methods=['POST'])
def user_signup():
    data = request.json
    required_fields = ['username', 'password', 'email', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    existing_user = User.query.filter(
        (User.username == data['username']) | (User.email == data['email'])
    ).first()
    if existing_user:
        return jsonify({"error": "Username or Email is already registered"}), 400

    new_user = User(
        username=data['username'],
        password=generate_password_hash(data['password']),
        email=data['email'],
        role=data['role']
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred during signup.", "details": str(e)}), 500

@app.route('/api/user/login', methods=['POST'])
def user_login():
    data = request.json
    required_fields = ['username', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Invalid Email or Password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }), 200


# Routes for Participants (Attendance Tracking System)
@app.route('/api/participant/signup', methods=['POST'])
def participant_signup():
    data = request.json

    # Validate input
    required_fields = ['student_Id', 'password', 'firstName', 'lastName', 'email', 'department']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Check if the student ID or email already exists
    existing_participant = Participant.query.filter(
        (Participant.student_Id == data['student_Id']) | (Participant.email == data['email'])
    ).first()
    if existing_participant:
        return jsonify({"error": "Student ID or Email is already registered"}), 400

    # Create a new participant
    new_participant = Participant(
        student_Id=data['student_Id'],
        password=generate_password_hash(data['password']),
        firstName=data['firstName'],
        lastName=data['lastName'],
        email=data['email'],
        department=data['department']
    )

    try:
        db.session.add(new_participant)
        db.session.commit()
        return jsonify({"message": "Participant registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred during signup.", "details": str(e)}), 500

@app.route('/api/participant/login', methods=['POST'])
def participant_login():
    data = request.json

    # Validate input
    required_fields = ['student_Id', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Find the participant by student_Id
    participant = Participant.query.filter_by(student_Id=data['student_Id']).first()
    if not participant or not check_password_hash(participant.password, data['password']):
        return jsonify({"error": "Invalid Student ID or Password"}), 401

    # Return success response
    return jsonify({
        "message": "Login successful",
        "participant": {
            "student_Id": participant.student_Id,
            "firstName": participant.firstName,
            "lastName": participant.lastName,
            "email": participant.email,
            "department": participant.department
        }
    }), 200

  #Displaying of Name and User that is logged in currently
@app.route('/api/participant/details', methods=['POST'])
def get_participant_details():
    data = request.json

    # Validate input
    if 'student_Id' not in data:
        return jsonify({"error": "'student_Id' is required"}), 400

    # Fetch the participant details
    participant = Participant.query.filter_by(student_Id=data['student_Id']).first()
    if not participant:
        return jsonify({"error": "Participant not found"}), 404

    return jsonify({
        "firstName": participant.firstName,
        "lastName": participant.lastName
    }), 200


#Event Registration

@app.route('/api/register', methods=['POST'])
def register_participant():
    data = request.json
    print(f"Incoming registration data: {data}")  # Log incoming data for debugging

    # List of required fields with validation
    required_fields = ['student_id', 'fullname', 'year_and_block', 'department', 'event_id']
    for field in required_fields:
        if field not in data or not data[field]:  # Check presence and non-emptiness
            error_message = f"Field '{field}' is missing or invalid."
            print(f"Validation error: {error_message}")  # Log missing/invalid field
            return jsonify({"error": error_message}), 400

        # Specific validation for event_id to allow integers
        if field == 'event_id' and not isinstance(data[field], (str, int)):
            error_message = f"Field '{field}' should be a valid string or integer."
            print(f"Validation error: {error_message}")
            return jsonify({"error": error_message}), 400

        # General validation for string fields
        if field != 'event_id' and not isinstance(data[field], str):
            error_message = f"Field '{field}' should be a valid string."
            print(f"Validation error: {error_message}")
            return jsonify({"error": error_message}), 400

    # Check if the participant is already registered for the event
    existing_registration = db.session.query(EventRegistration).filter_by(
        student_id=data['student_id'], event_id=data['event_id']
    ).first()
    
    if existing_registration:
        print(f"Duplicate registration attempt for student_id: {data['student_id']}, event_id: {data['event_id']}")
        return jsonify({"error": "You are already registered for this event."}), 400

    # Create a new registration record
    new_registration = EventRegistration(
        student_id=data['student_id'],
        fullname=data['fullname'],
        year_and_block=data['year_and_block'],
        department=data['department'],
        event_id=data['event_id'],  # The event ID from the frontend
        registration_date=datetime.utcnow(),  # Real-time registration timestamp
        registration_status="registered"  # Status defaults to 'registered'
    )

    try:
        # Save the registration in the database
        db.session.add(new_registration)
        db.session.commit()
        print(f"Registration successful for student_id: {data['student_id']}, event_id: {data['event_id']}")
        return jsonify({"message": "Registration successful!"}), 201
    except Exception as e:
        db.session.rollback()
        error_details = traceback.format_exc()
        print(f"Database error during registration: {error_details}")  # Log detailed error for debugging
        return jsonify({
            "error": "An unexpected error occurred during registration. Please try again later.",
            "details": str(e)  # Include error details for API clients if needed
        }), 500


# Fetching Registered Students
@app.route('/api/event_registration/<int:event_id>', methods=['GET'])
def get_event_registration(event_id):
    registrations = EventRegistration.query.filter_by(event_id=event_id).all()
    
    result = []
    for reg in registrations:
        result.append({
            "student_id": reg.student_id,
            "fullname": reg.fullname,
            "year_and_block": reg.year_and_block,
            "department": reg.department,
            "registration_date": reg.registration_date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # Return an empty list if no registrations exist
    return jsonify({"event_id": event_id, "registrations": result}), 200

# Fetching Attendance for an Event
@app.route('/api/event_attendance/<int:event_id>', methods=['GET'])
def get_event_attendance(event_id):
    attendance_records = Attendance.query.filter_by(event_id=event_id).all()
    
    result = []
    for record in attendance_records:
        result.append({
            "student_id": record.student_id,
            "fullname": record.fullName,
            "year_and_block": record.year_and_block,
            "department": record.department,
            "check_in": record.check_in.strftime('%Y-%m-%d %H:%M:%S') if record.check_in else None,
            "check_out": record.check_out.strftime('%Y-%m-%d %H:%M:%S') if record.check_out else None,
            "status": record.status
        })
    
    # Return an empty list if no attendance records exist
    return jsonify({"event_id": event_id, "attendance": result}), 200



# ATTENDANCE
@app.route('/api/attendance', methods=['POST'])
def record_attendance():
    data = request.json

    # Validate required fields
    required_fields = ['event_id', 'student_id', 'fullname', 'year_and_block', 'department']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Check for existing attendance record
        existing_attendance = Attendance.query.filter_by(
            event_id=data['event_id'],
            student_id=data['student_id']
        ).first()

        if existing_attendance:
            # Update the check_out field if it is the second scan
            if existing_attendance.check_out is None:
                existing_attendance.check_out = datetime.utcnow().strftime('%m-%d-%Y %H:%M:%S')
                db.session.commit()
                return jsonify({'message': 'Check-out recorded successfully'}), 200
            else:
                return jsonify({'error': 'Attendance already completed'}), 409

        # Add new attendance record
        new_attendance = Attendance(
            event_id=data['event_id'],
            student_id=data['student_id'],
            fullName=data['fullname'], 
            year_and_block=data['year_and_block'],  # Ensure this is passed as a string
            department=data['department'],
            check_in=data.get('check_in', datetime.utcnow().strftime('%m-%d-%Y %H:%M:%S')),  # Use formatted current time if missing
            check_out=None,  # Set check_out to None for the first scan
            status=data.get('status', 'Absent')  # Default to 'Absent' if not provided
        )
        db.session.add(new_attendance)
        db.session.commit()

        return jsonify({'message': 'Check-in recorded successfully'}), 201

    except Exception as e:
        print(f"Error: {e}")
        print("Received data:", data)
        return jsonify({'error': 'Failed to record attendance'}), 500


#qr generation
@app.route('/api/events/<int:event_id>/generate-qr', methods=['GET'])
def generate_qr_code(event_id):
    # Fetch event data from the database
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    # Prepare QR code data
    qr_data = f"{event.event_id},{event.event_name},{event.location}"
    qr = qrcode.make(qr_data)
    
    # Convert QR code to Base64
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return jsonify({
        "qr_code": qr_code_base64,
        "event_name": event.event_name
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

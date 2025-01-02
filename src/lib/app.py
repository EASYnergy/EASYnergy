from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import date
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

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
    attendance_ID = db.Column(db.Integer, primary_key=True)
    event_ID = db.Column(db.Integer, db.ForeignKey('event.event_id'))
    participant_ID = db.Column(db.Integer)
    check_in = db.Column(db.String(250))
    status = db.Column(db.String(20))
    remarks = db.Column(db.Text)

class Participant(db.Model):
    __tablename__ = 'participant'
    student_Id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(256))
    firstName = db.Column(db.String(256))
    lastName = db.Column(db.String(256))
    email = db.Column(db.String(256))
    department = db.Column(db.Text)
# Routes
        
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
                "participant_id": participant.participant_Id,
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

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.json
    required_fields = ['event_name', 'event_description', 'location', 'event_date', 'start_time', 'end_time']

    # Validate the payload
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Validate date and time formats
    try:
        event_date = date.fromisoformat(data['event_date'])  # Validate event_date
        start_time = data['start_time']  # Assuming correct format from the frontend
        end_time = data['end_time']  # Assuming correct format from the frontend
    except ValueError as ve:
        return jsonify({"error": f"Invalid date/time format: {ve}"}), 400

    # Create the event object
    new_event = Event(
    event_name=data['event_name'],
    event_description=data['event_description'],
    location=data['location'],
    event_date=event_date,
    start_time=start_time,
    end_time=end_time,
    speaker=data.get('speaker', ''),  # Provide a default value for speaker
)


    try:
        db.session.add(new_event)
        db.session.commit()
        return jsonify({"message": "Event created successfully", "event_id": new_event.event_id}), 201
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating event: {str(e)}")
        return jsonify({"error": "An error occurred during event creation.", "details": str(e)}), 500


@app.route('/registrations/<int:event_id>', methods=['GET'])
def get_registrations(event_id):
    attendance_records = Attendance.query.filter_by(event_ID=event_id).count()
    return jsonify({"event_id": event_id, "registration_count": attendance_records}), 200

@app.route('/register', methods=['POST'])
def register_participant():
    data = request.json

    # Validate input
    required_fields = ['participant_id', 'firstName', 'lastName', 'email', 'department', 'event_name']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required."}), 400

    # Check for existing registration for the same event
    existing_participant = Participant.query.filter_by(email=data['email']).first()
    if existing_participant:
        return jsonify({"error": "You are already registered."}), 400

    new_participant = Participant(
        firstName=data['firstName'],
        lastName=data['lastName'],
        email=data['email'],
        department=data['department']
    )

    try:
        db.session.add(new_participant)
        db.session.commit()
        return jsonify({"message": "Registration successful!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred during registration.", "details": str(e)}), 500

@app.route('/api/reports', methods=['GET'])
def get_report():
    today = date.today()

    # Total number of events
    total_events = Event.query.count()

    # Upcoming events (event_date > today)
    upcoming_events = Event.query.filter(Event.event_date > today).count()

    # Completed events (event_date < today)
    completed_events = Event.query.filter(Event.event_date < today).count()

    return jsonify({
        "total_events": total_events,
        "upcoming_events": upcoming_events,
        "completed_events": completed_events
    }), 200

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the event.", "details": str(e)}), 500
    
 #participant signup 

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json

    # Validate input
    required_fields = ['student_Id', 'password', 'firstName', 'lastName', 'email', 'department']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Check if the student ID or email already exists
    existing_user = Participant.query.filter(
        (Participant.student_Id == data['student_Id']) | 
        (Participant.email == data['email'])
    ).first()
    if existing_user:
        return jsonify({"error": "Student ID or Email is already registered"}), 400

    # Create a new participant
    new_participant = Participant(
        student_Id=data['student_Id'],
        password=generate_password_hash(data['password']),  # Securely hash the password
        firstName=data['firstName'],
        lastName=data['lastName'],
        email=data['email'],
        department=data['department']
    )

    try:
        db.session.add(new_participant)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred during signup.", "details": str(e)}), 500
    
#participant Login


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json

    # Validate input
    required_fields = ['student_Id', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Find the user by student_Id
    user = Participant.query.filter_by(student_Id=data['student_Id']).first()
    if not user:
        return jsonify({"error": "Invalid Student ID or Password"}), 401

    # Check the password
    if not check_password_hash(user.password, data['password']):
        return jsonify({"error": "Invalid Student ID or Password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "student_Id": user.student_Id,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "department": user.department
        }
    }), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables based on models
    app.run(debug=True)

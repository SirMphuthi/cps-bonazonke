# app/models.py

from . import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

# --- Association Tables for Many-to-Many Relationships ---

drone_flightplan_association = db.Table('drone_flightplan_association',
    db.Column('drone_id', db.Integer, db.ForeignKey('drone.id'), primary_key=True),
    db.Column('flight_plan_id', db.Integer, db.ForeignKey('flight_plan.id'), primary_key=True)
)

# --- NEW ---
# This table links Ground Units to Incidents
incident_ground_unit_association = db.Table('incident_ground_unit_association',
    db.Column('incident_id', db.Integer, db.ForeignKey('incident.id'), primary_key=True),
    db.Column('ground_unit_id', db.Integer, db.ForeignKey('ground_unit.id'), primary_key=True)
)


# --- Main Models ---

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='operator')
    
    incidents = db.relationship('Incident', back_populates='reporter', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Station(db.Model):
    __tablename__ = 'station'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    drones = db.relationship('Drone', back_populates='station', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Station {self.name}>'


# --- UPDATED ---
class Drone(db.Model):
    __tablename__ = 'drone'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default='AVAILABLE')
    battery_level = db.Column(db.Integer, nullable=False, default=100)
    current_latitude = db.Column(db.Float, nullable=False)
    current_longitude = db.Column(db.Float, nullable=False)
    video_feed_url = db.Column(db.String(255), nullable=True) # <-- NEW FIELD
    
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    station = db.relationship('Station', back_populates='drones')
    flight_plans = db.relationship('FlightPlan', secondary=drone_flightplan_association, back_populates='drones', lazy='dynamic')

    def __repr__(self):
        return f'<Drone {self.id}>'


# --- NEW ---
class GroundUnit(db.Model):
    __tablename__ = 'ground_unit'
    id = db.Column(db.Integer, primary_key=True)
    call_sign = db.Column(db.String(50), unique=True, nullable=False) # e.g., "SW-Response-1"
    status = db.Column(db.String(50), default='AVAILABLE') # e.g., AVAILABLE, EN_ROUTE, ON_SCENE
    current_latitude = db.Column(db.Float, nullable=False)
    current_longitude = db.Column(db.Float, nullable=False)

    # Relationship back to incidents
    incidents = db.relationship('Incident', secondary=incident_ground_unit_association, back_populates='ground_units')
    
    def __repr__(self):
        return f'<GroundUnit {self.call_sign}>'


# --- UPDATED ---
class Incident(db.Model):
    __tablename__ = 'incident'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='REPORTED')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reporter = db.relationship('User', back_populates='incidents')
    
    flight_plan = db.relationship('FlightPlan', back_populates='incident', uselist=False, cascade="all, delete-orphan")
    
    # New relationship to track assigned ground units
    ground_units = db.relationship('GroundUnit', secondary=incident_ground_unit_association, back_populates='incidents')

    def __repr__(self):
        return f'<Incident {self.id}>'


class FlightPlan(db.Model):
    __tablename__ = 'flight_plan'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default='PENDING_APPROVAL')
    clearance_code = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'), unique=True, nullable=False)
    incident = db.relationship('Incident', back_populates='flight_plan')
    drones = db.relationship('Drone', secondary=drone_flightplan_association, back_populates='flight_plans', lazy='dynamic')

    def __repr__(self):
        return f'<FlightPlan {self.id} - {self.status}>'

from . import db
from sqlalchemy.sql import func

# This is a helper table for the many-to-many relationship
# between Drones and FlightPlans. One drone could be part of multiple
# flight plans over its lifetime, and a single complex flight plan
# could potentially involve multiple drones.
drone_flightplan_association = db.Table('drone_flightplan_association',
    db.Column('drone_id', db.Integer, db.ForeignKey('drone.id'), primary_key=True),
    db.Column('flight_plan_id', db.Integer, db.ForeignKey('flight_plan.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Store a secure hash of the password, not the password itself
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='operator') # e.g., 'operator', 'admin'
    
    # Relationship: A user can report many incidents
    incidents = db.relationship('Incident', back_populates='reporter', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Station(db.Model):
    __tablename__ = 'station'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Relationship: A station has many drones
    drones = db.relationship('Drone', back_populates='station', lazy=True)

    def __repr__(self):
        return f'<Station {self.name}>'

class Drone(db.Model):
    __tablename__ = 'drone'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default='AVAILABLE')
    battery_level = db.Column(db.Integer, nullable=False, default=100)
    
    # Relationships
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    station = db.relationship('Station', back_populates='drones')
    flight_plans = db.relationship('FlightPlan', secondary=drone_flightplan_association, back_populates='drones', lazy='dynamic')

    def __repr__(self):
        return f'<Drone {self.id}>'

class Incident(db.Model):
    __tablename__ = 'incident'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='REPORTED')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reporter = db.relationship('User', back_populates='incidents')
    flight_plan = db.relationship('FlightPlan', back_populates='incident', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Incident {self.id}>'

class FlightPlan(db.Model):
    __tablename__ = 'flight_plan'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default='PENDING_APPROVAL')
    clearance_code = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    incident_id = db.Column(db.Integer, db.ForeignKey('incident.id'), unique=True, nullable=False)
    incident = db.relationship('Incident', back_populates='flight_plan')
    drones = db.relationship('Drone', secondary=drone_flightplan_association, back_populates='flight_plans', lazy='dynamic')

    def __repr__(self):
        return f'<FlightPlan {self.id} - {self.status}>'

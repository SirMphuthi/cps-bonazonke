from flask import Blueprint, request, jsonify
from .models import Station, Drone, User, Incident, FlightPlan, GroundUnit, db
from .services import report_and_dispatch_drone, calculate_hotspots
from flask_jwt_extended import create_access_token, jwt_required

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'username' not in data or not 'password' in data:
        return jsonify({'error': 'Missing username or password'}), 400
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'username': new_user.username}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data:
        return jsonify({'error': 'Missing username or password'}), 400
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)

@api.route('/stations', methods=['POST', 'GET'])
@jwt_required()
def handle_stations():
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(key in data for key in ['name', 'latitude', 'longitude']):
            return jsonify({'error': 'Missing required fields'}), 400
        new_station = Station(name=data['name'], latitude=data['latitude'], longitude=data['longitude'])
        db.session.add(new_station)
        db.session.commit()
        return jsonify({'id': new_station.id, 'name': new_station.name, 'latitude': new_station.latitude, 'longitude': new_station.longitude}), 201
    if request.method == 'GET':
        stations_list = Station.query.all()
        stations_data = [{'id': s.id, 'name': s.name, 'latitude': s.latitude, 'longitude': s.longitude} for s in stations_list]
        return jsonify(stations_data)

@api.route('/stations/<int:station_id>', methods=['GET', 'DELETE'])
@jwt_required()
def handle_station(station_id):
    station = Station.query.get_or_404(station_id)
    if request.method == 'GET':
        return jsonify({'id': station.id, 'name': station.name, 'latitude': station.latitude, 'longitude': station.longitude})
    if request.method == 'DELETE':
        db.session.delete(station)
        db.session.commit()
        return jsonify({'message': f'Station {station.name} with id {station_id} has been deleted.'})

@api.route('/ground-units', methods=['POST', 'GET'])
@jwt_required()
def handle_ground_units():
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(key in data for key in ['call_sign', 'latitude', 'longitude']):
            return jsonify({'error': 'Missing required fields'}), 400
        new_unit = GroundUnit(call_sign=data['call_sign'], current_latitude=data['latitude'], current_longitude=data['longitude'])
        db.session.add(new_unit)
        db.session.commit()
        return jsonify({'id': new_unit.id, 'call_sign': new_unit.call_sign, 'status': new_unit.status}), 201
    if request.method == 'GET':
        units_list = GroundUnit.query.all()
        units_data = [{'id': u.id, 'call_sign': u.call_sign, 'status': u.status} for u in units_list]
        return jsonify(units_data)

@api.route('/drones', methods=['POST', 'GET'])
@jwt_required()
def handle_drones():
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(key in data for key in ['station_id', 'battery_level']):
            return jsonify({'error': 'Missing required fields: station_id, battery_level'}), 400
        station = Station.query.get(data['station_id'])
        if not station:
            return jsonify({'error': 'Station not found'}), 404
        new_drone = Drone(station_id=data['station_id'], battery_level=data['battery_level'], current_latitude=station.latitude, current_longitude=station.longitude)
        db.session.add(new_drone)
        db.session.commit()
        return jsonify({'id': new_drone.id, 'station_id': new_drone.station_id, 'status': new_drone.status, 'battery_level': new_drone.battery_level}), 201
    if request.method == 'GET':
        drones_list = Drone.query.all()
        drones_data = [{'id': d.id, 'station_id': d.station_id, 'status': d.status, 'battery_level': d.battery_level, 'current_latitude': d.current_latitude, 'current_longitude': d.current_longitude} for d in drones_list]
        return jsonify(drones_data)

@api.route('/drones/<int:drone_id>', methods=['GET'])
@jwt_required()
def get_drone(drone_id):
    drone = Drone.query.get_or_404(drone_id)
    return jsonify({'id': drone.id, 'station_id': drone.station_id, 'status': drone.status, 'battery_level': drone.battery_level, 'current_latitude': drone.current_latitude, 'current_longitude': drone.current_longitude})

@api.route('/incidents', methods=['POST', 'GET'])
@jwt_required()
def handle_incidents():
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(key in data for key in ['latitude', 'longitude', 'description', 'reporter_id']):
            return jsonify({'error': 'Missing required fields'}), 400
        user = User.query.get(data['reporter_id'])
        if not user:
            return jsonify({'error': f"User with id {data['reporter_id']} not found."}), 404
        incident = report_and_dispatch_drone(data)
        return jsonify({'message': 'Incident reported successfully.', 'incident_id': incident.id, 'incident_status': incident.status}), 201
    if request.method == 'GET':
        incidents_list = Incident.query.all()
        incidents_data = [{'id': i.id, 'status': i.status, 'description': i.description, 'latitude': i.latitude, 'longitude': i.longitude} for i in incidents_list]
        return jsonify(incidents_data)

@api.route('/incidents/<int:incident_id>', methods=['GET', 'PATCH'])
@jwt_required()
def handle_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    if request.method == 'GET':
        return jsonify({'id': incident.id, 'status': incident.status, 'description': incident.description, 'latitude': incident.latitude, 'longitude': incident.longitude})
    if request.method == 'PATCH':
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'error': 'Missing required field: status'}), 400
        incident.status = data['status']
        db.session.commit()
        return jsonify({'id': incident.id, 'status': incident.status, 'description': incident.description})

@api.route('/flightplans', methods=['GET'])
@jwt_required()
def get_flightplans():
    plans_list = FlightPlan.query.all()
    plans_data = [{'id': p.id, 'incident_id': p.incident_id, 'status': p.status, 'clearance_code': p.clearance_code} for p in plans_list]
    return jsonify(plans_data)

@api.route('/analytics/hotspots', methods=['GET'])
@jwt_required()
def get_hotspots():
    hotspots = calculate_hotspots()
    return jsonify(hotspots)

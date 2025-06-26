from . import db
from .models import Drone, Incident, FlightPlan, Station
from .atc_service import request_airspace_clearance
from geopy.distance import geodesic
import math

def find_closest_available_drone(incident_coords):
    available_drones = Drone.query.filter_by(status='AVAILABLE').all()
    if not available_drones:
        return None

    closest_drone = None
    min_distance = float('inf')

    for drone in available_drones:
        drone_coords = (drone.current_latitude, drone.current_longitude)
        distance = geodesic(drone_coords, incident_coords).kilometers
        
        if distance < min_distance:
            min_distance = distance
            closest_drone = drone
            
    return closest_drone

def report_and_dispatch_drone(incident_data):
    new_incident = Incident(
        latitude=incident_data['latitude'],
        longitude=incident_data['longitude'],
        description=incident_data['description'],
        reporter_id=incident_data['reporter_id']
    )
    db.session.add(new_incident)
    
    incident_coords = (new_incident.latitude, new_incident.longitude)
    closest_drone = find_closest_available_drone(incident_coords)
    
    if not closest_drone:
        new_incident.status = 'NO_DRONES_AVAILABLE'
        db.session.commit()
        return new_incident

    new_incident.status = 'AWAITING_AIRSPACE_CLEARANCE'

    new_flight_plan = FlightPlan(incident=new_incident)
    new_flight_plan.drones.append(closest_drone)
    db.session.add(new_flight_plan)
    
    flight_plan_data = {
        "drone_id": closest_drone.id,
        "incident_location": incident_coords
    }
    atc_response = request_airspace_clearance(flight_plan_data)
    
    if atc_response['status'] == 'APPROVED':
        new_flight_plan.status = 'APPROVED'
        new_flight_plan.clearance_code = atc_response['clearance_code']
        closest_drone.status = 'IN_TRANSIT'
        new_incident.status = 'DRONE_DISPATCHED'
    else:
        new_flight_plan.status = 'REJECTED'
        new_incident.status = 'AIRSPACE_RESTRICTED'
    
    db.session.commit()
    return new_incident

def calculate_hotspots(grid_size=0.5):
    incidents = Incident.query.all()
    if not incidents:
        return []

    grid = {}

    for incident in incidents:
        lat_key = round(incident.latitude / grid_size) * grid_size
        lon_key = round(incident.longitude / grid_size) * grid_size
        grid_key = (lat_key, lon_key)
        
        if grid_key not in grid:
            grid[grid_key] = 0
        grid[grid_key] += 1
    
    hotspots = []
    for key, count in grid.items():
        if count > 2:
            hotspots.append({
                "latitude": key[0],
                "longitude": key[1],
                "incident_count": count
            })
            
    sorted_hotspots = sorted(hotspots, key=lambda x: x['incident_count'], reverse=True)
    
    return sorted_hotspots[:5]

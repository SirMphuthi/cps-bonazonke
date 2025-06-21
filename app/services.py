from . import db
from .models import Drone, Incident, FlightPlan
from .atc_service import request_airspace_clearance

def report_and_dispatch_drone(incident_data):
    """
    Main service function to handle a new incident report.
    """
    # Step 1: Create the Incident record
    new_incident = Incident(
        latitude=incident_data['latitude'],
        longitude=incident_data['longitude'],
        description=incident_data['description'],
        reporter_id=incident_data['reporter_id']
    )
    db.session.add(new_incident)
    
    # Step 2: Find the first available drone
    # A real system would calculate the closest, but this is good for now.
    available_drone = Drone.query.filter_by(status='AVAILABLE').first()
    
    if not available_drone:
        new_incident.status = 'NO_DRONES_AVAILABLE'
        db.session.commit()
        print("DISPATCH SERVICE: No drones available.")
        return new_incident # Return the incident with its updated status

    print(f"DISPATCH SERVICE: Found available drone: {available_drone.id}")
    new_incident.status = 'AWAITING_AIRSPACE_CLEARANCE'

    # Step 3: Create a Flight Plan for submission
    new_flight_plan = FlightPlan(incident=new_incident)
    new_flight_plan.drones.append(available_drone) # Associate the drone with the flight plan
    db.session.add(new_flight_plan)
    
    # Step 4: Request Airspace Clearance from mock ATC service
    flight_plan_data = {
        "drone_id": available_drone.id,
        "incident_location": (new_incident.latitude, new_incident.longitude)
    }
    atc_response = request_airspace_clearance(flight_plan_data)
    
    # Step 5: Handle ATC Response
    if atc_response['status'] == 'APPROVED':
        print(f"DISPATCH SERVICE: ATC Approved. Dispatching drone.")
        new_flight_plan.status = 'APPROVED'
        new_flight_plan.clearance_code = atc_response['clearance_code']
        available_drone.status = 'IN_TRANSIT'
        new_incident.status = 'DRONE_DISPATCHED'
    else:
        print(f"DISPATCH SERVICE: ATC Rejected. Drone cannot be dispatched.")
        new_flight_plan.status = 'REJECTED'
        new_incident.status = 'AIRSPACE_RESTRICTED'
    
    db.session.commit()
    return new_incident

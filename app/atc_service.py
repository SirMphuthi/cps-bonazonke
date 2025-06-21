import random
import time
import uuid

def request_airspace_clearance(flight_plan_data):
    """
    Simulates sending a flight plan to the CAA/ATC for approval.
    """
    print(f"ATC Service: Received flight plan for Drone ID {flight_plan_data['drone_id']}.")
    
    # Simulate network delay and processing time of a real API call
    print("ATC Service: Awaiting clearance...")
    time.sleep(3) # Pauses for 3 seconds
    
    # 90% chance of approval for simulation purposes
    if random.random() < 0.9:
        clearance_code = str(uuid.uuid4()).upper()
        print(f"ATC Service: Flight plan APPROVED. Clearance code: {clearance_code}")
        return {"status": "APPROVED", "clearance_code": clearance_code}
    else:
        print("ATC Service: Flight plan REJECTED. Airspace is busy.")
        return {"status": "REJECTED", "clearance_code": None}

def close_flight_plan(clearance_code):
    """
    Simulates notifying the ATC that the flight is complete.
    """
    print(f"ATC Service: Received notification to close flight with code {clearance_code}.")
    return {"status": "CLOSED"}

from app import create_app, db
from app.models import Station, User, Drone, FlightPlan, Incident, drone_flightplan_association

# Create an application context
app = create_app()
app.app_context().push()

def seed_database():
    """Wipes and seeds the database with sample data."""
    
    print("Wiping old data...")
    # --- WIPE DATA IN THE CORRECT ORDER ---
    # 1. Clear the association table first
    db.session.execute(drone_flightplan_association.delete())
    
    # 2. Clear the tables that have foreign keys pointing to others
    FlightPlan.query.delete()
    Incident.query.delete()
    Drone.query.delete()
    
    # 3. Now it's safe to clear the primary tables
    User.query.delete()
    Station.query.delete()
    
    db.session.commit()
    print("Old data wiped.")

    print("Seeding new data...")

    # --- Create Users ---
    user1 = User(username='operator1')
    user1.set_password('password123')
    user2 = User(username='operator2')
    user2.set_password('password456')
    
    db.session.add(user1)
    db.session.add(user2)
    print("Users created.")

    # --- Create Stations ---
    station1 = Station(name="Soweto Central Drone Hub", latitude=-26.2683, longitude=27.8593)
    station2 = Station(name="Sandton City Command", latitude=-26.1076, longitude=28.0567)
    station3 = Station(name="Rosebank Drone Port", latitude=-26.1467, longitude=28.0423)
    
    db.session.add(station1)
    db.session.add(station2)
    db.session.add(station3)
    print("Stations created.")

    # We must commit here so that the stations get an ID before we assign drones
    db.session.commit()
    print("Committing users and stations.")

    # --- Create Drones ---
    drone1 = Drone(station_id=station1.id, battery_level=100, current_latitude=station1.latitude, current_longitude=station1.longitude)
    drone2 = Drone(station_id=station1.id, battery_level=100, current_latitude=station1.latitude, current_longitude=station1.longitude)
    drone3 = Drone(station_id=station2.id, battery_level=100, current_latitude=station2.latitude, current_longitude=station2.longitude)
    drone4 = Drone(station_id=station3.id, battery_level=100, current_latitude=station3.latitude, current_longitude=station3.longitude)
    
    db.session.add_all([drone1, drone2, drone3, drone4])
    print("Drones created.")
    
    # Final commit
    db.session.commit()
    print("Database has been seeded successfully!")


if __name__ == '__main__':
    seed_database()

# COMMUNITY PROTECTION SERVICE (CPS) #BONAZONKE

**Tagline:** *#BONAZONKE (See Everything)*

## 1. Overview

The Community Protection Service (CPS) is a backend application designed to power a next-generation, rapid-response security system for urban communities. The core concept is to drastically reduce response times to crime alerts by leveraging a network of automated surveillance drones dispatched from local stations.

When an incident is reported, the system identifies the nearest available drone, requests airspace clearance from a simulated aviation authority, and dispatches the drone to provide real-time aerial footage and location data to ground support units. This project serves as the foundational backend framework for such a system.

This project was developed to meet the criteria of the Web Stack Portfolio Project, focusing on backend architecture, API design, database management, and simulating real-world regulatory compliance.

---

## 2. Project Architecture

The application is built using the Flask micro-framework for Python, following a structured and scalable design pattern.

* **Backend Framework:** **Python** with **Flask**.
* **Database:** **PostgreSQL** is used for its robustness and powerful features.
* **Object-Relational Mapper (ORM):** **Flask-SQLAlchemy** provides a high-level interface to the database, mapping Python objects to database tables.
* **Database Migrations:** **Flask-Migrate** (using Alembic) handles all database schema changes, allowing the data model to evolve safely over time.
* **Environment Management:** Python's built-in **`venv`** module is used for creating an isolated project environment and managing dependencies.
* **API Documentation:** **Flasgger** is used to automatically generate interactive API documentation via Swagger UI.
* **Regulatory Simulation:** A dedicated **`atc_service.py`** module simulates the essential process of filing a flight plan and requesting airspace clearance from a Civil Aviation Authority (CAA), adding a critical layer of real-world complexity.


### Directory Structure

The project is organized to separate concerns, making it clean, maintainable, and scalable.

```
/cps-bonazonke
|
├── app/
│   ├── __init__.py         # Initializes the Flask app and its extensions
│   ├── models.py           # SQLAlchemy data model classes (Incident, Drone, FlightPlan, etc.)
│   ├── routes.py           # Defines all API endpoints (e.g., /api/incidents)
│   ├── services.py         # Contains the core business logic (e.g., dispatching a drone)
│   ├── atc_service.py      # Simulates communication with Air Traffic Control
│   └── config.py           # Configuration settings (e.g., database URI)
|
├── migrations/             # Stores the database migration scripts
├── tests/                  # All project tests will live here
├── venv/                   # The Python virtual environment directory (ignored by Git)
├── .env                    # For storing secret environment variables
├── .gitignore              # Specifies files for Git to ignore
├── requirements.txt        # A list of all Python packages required for the project
└── README.md               # This documentation file
```


---


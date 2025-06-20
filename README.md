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
---

## 3. Setup and Installation

To run this project locally, you will need **Python 3.8+** and **PostgreSQL** installed on your Linux system.

### Step 1: Clone the Repository

```bash
git clone [https://github.com/your-username/cps-bonazonke.git](https://github.com/your-username/cps-bonazonke.git)
cd cps-bonazonke
```

### Step 2: Create and Activate Virtual Environment

This isolates the project's dependencies from your global Python installation.

```bash
python3 -m venv venv
source venv/bin/activate
```
*(You must run `source venv/bin/activate` every time you open a new terminal to work on this project.)*

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```
*(Note: We will populate the `requirements.txt` file during the development phase.)*

### Step 4: Set Up PostgreSQL Database

You need to create a dedicated user and database for the application.

```bash
# Log in to PostgreSQL as the default superuser
sudo -u postgres psql

# Create a new database for the project
CREATE DATABASE cps_db;

# Create a new user and password (replace 'password' with a strong password)
CREATE USER cps_user WITH PASSWORD 'password';

# Grant all privileges for the new database to the new user
GRANT ALL PRIVILEGES ON DATABASE cps_db TO cps_user;

# Exit the psql shell
\q
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root to store your secret configurations.

```bash
# Create the .env file
touch .env
```

Now, open the `.env` file and add the following lines, replacing the password if you chose a different one.

```
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL="postgresql://cps_user:password@localhost/cps_db"
```

---

## 4. Database Migrations

Before running the app for the first time, and any time you change the data models in `app/models.py`, you must run migrations to update the database schema.

```bash
# To initialize the migrations folder (only run this once)
flask db init

# To generate a new migration script after changing a model
flask db migrate -m "Describe the change you made"

# To apply the migration to the database
flask db upgrade
```

---

## 5. Running the Application

Once the setup is complete, you can run the development server.

```bash
flask run
```

The API will be available at `http://localhost:5000`.

---

## 6. API Documentation

Full, interactive API documentation is automatically generated and available via Swagger UI once the application is running.

* **Swagger UI URL:** `http://localhost:5000/apidocs`

### Key Endpoints

* `POST /api/incidents`: Report a new crime incident. The system will automatically attempt to find a drone and get airspace clearance.
* `GET /api/incidents/<id>`: Check the status of a specific incident. The status may reflect the ATC clearance process (e.g., `AWAITING_AIRSPACE_CLEARANCE`).
* `GET /api/drones`: View the status of all drones in the fleet.
* `GET /api/flightplans`: View the status of recent or active flight plans submitted to the ATC.

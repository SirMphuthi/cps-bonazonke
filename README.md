# Community Protection Service (CPS) #BONAZONKE

### Developed by Kgotso Mphuthi

## 1. Project Overview

Welcome to my web stack portfolio project. For this project, I developed the **Community Protection Service (CPS)**, a backend framework designed to tackle the real-world problem of slow emergency response times in urban areas.

My goal was to design and build a robust, scalable system that could serve as the core logic for a network of automated surveillance drones. The system manages incident reports, identifies available drones, and simulates a flight clearance process with an aviation authority before dispatching a unit. This project demonstrates my ability to architect a complete backend solution from the ground up to solve a complex problem.

## 2. Technology Choices & Architecture

I carefully selected the following technologies to build a robust and modern application, keeping flexibility, reliability, and professional standards in mind.

* **Language: Python**
    * **Why I chose it:** I selected Python for its clean, readable syntax and its powerful ecosystem of libraries, which is perfectly suited for rapid backend development.

* **Framework: Flask**
    * **Why I chose it:** I chose Flask, a micro-framework, because it provided me with the flexibility to design the application's architecture from scratch. This allowed me to implement professional patterns like application factories and service layers without being constrained by a more opinionated framework.

* **Database: PostgreSQL**
    * **Why I chose it:** For an application dealing with critical data, reliability is key. I chose PostgreSQL for its proven robustness, data integrity features, and strong performance with complex queries.

* **ORM: Flask-SQLAlchemy & Flask-Migrate**
    * **Why I chose them:** I used SQLAlchemy to interact with the database in a more Pythonic way, which abstracts away raw SQL and reduces potential errors. To manage the evolution of the database schema safely as I developed the models, I integrated Flask-Migrate.

* **API Documentation: Flasgger**
    * **Why I chose it:** Since this is a backend-only project, clear documentation is essential. I implemented Flasgger to auto-generate a live, interactive Swagger UI page, making my API easily understandable and testable for anyone.

### Architectural Design

I designed the application architecture with a focus on the "Separation of Concerns" principle to ensure the codebase is clean, maintainable, and scalable.

```
/cps-bonazonke
|
├── app/
│   ├── __init__.py         # Application factory where the app is created and configured
│   ├── config.py           # Handles environment configurations
│   ├── models.py           # Contains all SQLAlchemy database models
│   ├── routes.py           # Defines all API endpoints (the "view" layer)
│   ├── services.py         # Contains complex business logic
│   └── atc_service.py      # Simulates the external Air Traffic Control service
|
├── migrations/             # Stores all database migration scripts
├── venv/                   # The Python virtual environment
├── .env                    # Local environment variables (not committed to Git)
├── .env.example            # A template for the .env file
├── requirements.txt        # A pinned list of all Python dependencies
├── run.py                  # The entry point to start the application
├── seed.py                 # My script to seed the database with sample data
└── README.md               # This documentation file
```

---

## 3. Local Setup and Installation

To get the project running on your local machine, please follow these steps. You will need Python 3.8+ and PostgreSQL installed.

#### Step 1: Clone the Repository
```bash
git clone [https://github.com/your-username/cps-bonazonke.git](https://github.com/your-username/cps-bonazonke.git)
cd cps-bonazonke
```

#### Step 2: Set Up the Environment
```bash
# Create and activate the Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all the required packages from the pinned list
pip install -r requirements.txt
```

#### Step 3: Set Up the PostgreSQL Database
```bash
# Log in to PostgreSQL as the default admin user
sudo -u postgres psql

# Create the database and user for this project
CREATE DATABASE cps_db;
CREATE USER cps_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE cps_db TO cps_user;
\q
```

#### Step 4: Configure Environment Variables
Create your local `.env` file by copying the template.
```bash
cp .env.example .env
```
Then, open the new `.env` file and ensure the `DATABASE_URL` is correct (the password is 'password' if you followed the step above).

---

## 4. Database Management

#### Migrations
Before running the app for the first time, and any time the models in `app/models.py` are changed, the database schema must be updated.
```bash
# To initialize the migrations folder (only run once per project)
flask db init

# To generate a new migration script
flask db migrate -m "A message describing the changes"

# To apply the changes to the database
flask db upgrade
```

#### Seeding the Database (Optional)
I have included a seed script to populate the database with a consistent set of sample data for testing and demonstration. This script will wipe existing data before populating.
```bash
python seed.py
```

---

## 5. Running the Application

Once the setup is complete, you can start the Flask development server.
```bash
flask run
```
The API will now be available at `http://127.0.0.1:5000`.

The API documentation is generated live and can be viewed in a web browser at: **`http://127.0.0.1:5000/apidocs`**

---

## 6. Future Enhancements

Looking ahead, I have identified several exciting potential enhancements for this project that would build upon the current foundation:

* **Asynchronous Operations:** Integrate a task queue like Celery and Redis to handle the simulated ATC clearance request asynchronously, preventing the API from blocking and providing a more responsive experience.
* **Real-time Dashboard:** Implement WebSockets to push live location updates of drones to a frontend, creating a real-time monitoring dashboard.
* **Token-Based Authentication:** Enhance the login system by generating secure JSON Web Tokens (JWT) to protect the API endpoints, which is standard practice for modern web services.
* **Advanced Dispatch Logic:** Improve the `services.py` logic to calculate the geographically closest drone, accounting for potential obstacles, instead of just selecting the first available unit.

---

Thank you for reviewing my project!

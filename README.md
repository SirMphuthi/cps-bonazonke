# Community Protection Service (CPS) #BONAZONKE

### Developed by Kgotso Mphuthi

## 1. Project Overview

Welcome to my web stack portfolio project. For this project, I developed the **Community Protection Service (CPS)**, a backend framework designed to tackle the real-world problem of slow emergency response times in urban areas.

My goal was to design and build a robust, scalable system that could serve as the core logic for a network of automated surveillance drones. The system manages incident reports, identifies available drones, and simulates a flight clearance process with an aviation authority before dispatching a unit. This project demonstrates my ability to architect a complete backend solution from the ground up to solve a complex problem.

## 2. Technology Choices & Architecture

I carefully selected the following technologies to build a robust and modern application, keeping flexibility, reliability, and professional standards in mind.

* **Language: Python** & **Framework: Flask**
    * **Why:** I chose Flask for its flexibility, which allowed me to design a custom architecture and implement professional patterns like application factories and service layers.
* **Database: PostgreSQL**
    * **Why:** For an application dealing with critical data, I chose PostgreSQL for its proven reliability and data integrity features.
* **ORM: Flask-SQLAlchemy & Flask-Migrate**
    * **Why:** I used SQLAlchemy to interact with the database in a more Pythonic way. To manage changes to the database schema safely as I developed the models, I integrated Flask-Migrate.
* **API Documentation: Flasgger**
    * **Why:** Clear documentation is essential. I implemented Flasgger to auto-generate a live, interactive Swagger UI page, making my API easily understandable and testable.

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
# Log into PostgreSQL as the default admin user
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
Now, open the new `.env` file and ensure the `DATABASE_URL` is correct (the password is 'password' if you followed Step 3 exactly).

---

## 4. Database Initialization

Before running the app for the first time, you must create the database tables.

1.  **Initialize the migrations folder** (only needs to be run once per project):
    ```bash
    flask db init
    ```
2.  **Generate the migration script:**
    ```bash
    flask db migrate -m "Initial database schema"
    ```
3.  **Apply the migrations to create the tables:**
    ```bash
    flask db upgrade
    ```
4.  **(Optional) Seed the database** with sample data for a clean demonstration. This script will wipe existing data first.
    ```bash
    python seed.py
    ```

---

## 5. Running the Application

Once the database is initialized, you can start the Flask development server. This terminal window must be kept running.
```bash
flask run
```
The API is now live and available at `http://127.0.0.1:5000`.

---

## 6. How to Test the API

Once the server is running, open a **second terminal** with the virtual environment activated (`source venv/bin/activate`). You can use the following `curl` commands to test the core end-to-end functionality.

1.  **Check the seeded stations:**
    ```bash
    curl [http://127.0.0.1:5000/api/stations](http://127.0.0.1:5000/api/stations)
    ```

2.  **Simulate reporting a new incident:**
    This tests the main workflow: creating an incident, finding a drone, and simulating an ATC request.
    ```bash
    curl -X POST [http://127.0.0.1:5000/api/incidents](http://127.0.0.1:5000/api/incidents) \
    -H "Content-Type: application/json" \
    -d '{
        "latitude": -26.2041,
        "longitude": 28.0473,
        "description": "Robbery in progress in Johannesburg Central.",
        "reporter_id": 1
    }'
    ```

3.  **Update the new incident's status** (assuming it has `id: 1`):
    ```bash
    curl -X PATCH [http://127.0.0.1:5000/api/incidents/1](http://127.0.0.1:5000/api/incidents/1) \
    -H "Content-Type: application/json" \
    -d '{"status": "RESOLVED"}'
    ```

4.  **Verify the update:**
    ```bash
    curl [http://127.0.0.1:5000/api/incidents/1](http://127.0.0.1:5000/api/incidents/1)
    ```

---

## 7. API Documentation

For a more detailed and interactive way to explore the API, I have integrated Flasgger to provide a live Swagger UI documentation page.

* **How to access:** While the Flask server is running, open your web browser and navigate to:
    **`http://127.0.0.1:5000/apidocs`**

This interactive page allows you to see all available endpoints, their expected parameters, and test them directly from the browser.

---

## Future Enhancements

Looking ahead, I have identified several exciting potential enhancements for this project that would build upon the current foundation:

* **Facial Recognition Integration:** Develop a separate microservice to handle image analysis. This service would receive images captured by drones at an incident scene and integrate with a mock Department of Home Affairs API to identify persons of interest, linking their identity back to the incident report. This demonstrates an understanding of microservice architecture and secure third-party API integration.

* **Asynchronous Task Handling:** Integrate a task queue like Celery with Redis to handle time-consuming operations like the ATC clearance request and facial recognition processing. This would prevent the API from blocking and create a more responsive and scalable system.

* **Real-time Monitoring Dashboard:** Implement WebSockets to push live location updates of drones and new incident alerts to a frontend application, creating a real-time command-and-control dashboard for operators.

* **Token-Based Authentication:** Enhance the login system by generating secure JSON Web Tokens (JWT) upon successful login. These tokens would then be required to access protected API endpoints, implementing a stateless and industry-standard security model.


---

## Copyright & License

© 2025 Kgotso Mphuthi. All Rights Reserved.

This software is the proprietary property of Kgotso Mphuthi. You are granted temporary permission to view the source code for the sole purpose of assessing my technical skills. No other rights are granted. You may not copy, modify, distribute, or use this software for any other purpose without my express written permission.

---

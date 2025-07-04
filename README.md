# Community Protection Service (CPS) #BONAZONKE

### Developed by Kgotso Mphuthi

---

## 1. Project Overview

Welcome to my web stack portfolio project. For this project, I developed the **Community Protection Service (CPS)**, a backend framework designed to tackle the real-world problem of slow emergency response times in urban areas, inspired by the needs of communities like my home in Soweto, Gauteng.

My goal was to architect and build a robust, secure, and intelligent system from the ground up. It serves as the core command-and-control logic for a network of automated surveillance drones and coordinated ground units. The system is not only reactive, responding to incidents by dispatching the **geographically closest drone** for the fastest response time, but also proactive, using data analysis to identify potential crime hotspots for preventative patrols.

This project showcases a full development lifecycle, from initial architectural design to implementing advanced business logic, data analysis, and professional-grade security.

## 2. Core Features Implemented

This is more than a simple CRUD application. I have engineered several advanced, real-world features to demonstrate a deep understanding of backend systems development:

* **Intelligent Asset Dispatch:** The system uses geospatial calculations (`geopy`) to identify and dispatch the drone that is geographically closest to a new incident, ensuring the fastest possible response time.
* **Predictive Hotspot Analysis:** An analytics endpoint (`/api/analytics/hotspots`) processes historical incident data to identify and report on high-density crime zones, enabling a shift from reactive to proactive policing.
* **Secure, Token-Based Authentication:** The entire API is secured using JSON Web Tokens (JWT). All data-centric endpoints are protected and require a valid token, which is obtained via a dedicated `/login` route that validates credentials against securely hashed passwords.
* **Simulated Third-Party Integration:** The dispatch service includes a simulation of communicating with an external Air Traffic Control (ATC) service, complete with realistic network delays, demonstrating the ability to design systems that integrate with external APIs.
* **Comprehensive Data Modeling:** The database schema is designed with clear relationships between multiple resources, including stations, drones, users, ground units, incidents, and flight plans, all managed via a professional migration workflow.

## 3. Technology Choices & Architecture

I carefully selected the following technologies to build a modern and professional application.

* **Language: Python** & **Framework: Flask**
* **Database Engine: SQLite**
* **ORM: Flask-SQLAlchemy & Flask-Migrate**
* **Geospatial Calculations: `geopy`**
* **Security: Flask-JWT-Extended**
* **API Documentation: Flasgger (Swagger)**
* **Demonstration Tool: `ngrok`**

My architectural approach focuses on a clean separation of concerns and plans for future growth by allowing complex features like image analysis to be built out as independent microservices.

---

## 4. Local Setup and Daily Workflow

This project was developed within an ephemeral Linux environment. The following steps outline both the one-time setup and the daily startup routine required to run the application in such an environment.

### One-Time Setup

These steps only need to be performed once when first cloning the project.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/cps-bonazonke.git](https://github.com/your-username/cps-bonazonke.git)
    cd cps-bonazonke
    ```
2.  **Configure Environment Variables:**
    ```bash
    cp .env.example .env
    ```
3.  **Initialize the Database Migrations Folder:**
    ```bash
    flask db init
    ```

### Daily Startup Routine

Because the environment is ephemeral, the virtual environment and installed packages may not persist between sessions. **This routine must be followed every time you start a new terminal session.**

1.  **Activate the Python Environment:**
    ```bash
    # First, create the venv if it doesn't exist
    python3 -m venv venv

    # Then, activate it
    source venv/bin/activate
    ```
2.  **Install All Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create/Update the Database:**
    ```bash
    flask db upgrade
    ```
4.  **(Recommended) Seed the Database:**
    ```bash
    python seed.py
    ```
5.  **Start the Server:** In your **first terminal**, run the application server.
    ```bash
    flask run --host=0.0.0.0
    ```

---

## 5. Testing the API

With the server running, open a **second terminal** and activate the environment (`source venv/bin/activate`). You must log in to get an access token before testing other features.

### Step 1: Log In and Get Your Token

Use the credentials for `operator1` (password: `password123`), which were created by the `seed.py` script.

```bash
curl -X POST [http://127.0.0.1:5000/api/login](http://127.0.0.1:5000/api/login) \
-H "Content-Type: application/json" \
-d '{
    "username": "operator1",
    "password": "password123"
}'
```

This will return an access_token. Copy the long string of characters inside the quotes.

### Step 2: Test a Protected Endpoint

Store the token in a shell variable and use it to access a protected route.

```bash
Replace <COPIED_TOKEN> with the actual token you copied
TOKEN="<COPIED_TOKEN>"
```

### Now, use the token to test the analytics endpoint

```bash
curl -H "Authorization: Bearer $TOKEN" [http://127.0.0.1:5000/api/analytics/hotspots](http://127.0.0.1:5000/api/analytics/hotspots)
```

### 6. Live API Documentation via ngrok

To view the interactive API documentation from an external browser, a secure tunnel is required. I have included ngrok in this project for that purpose.

One-Time ngrok Setup
Download ngrok:

```bash

curl -L [https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz](https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz) --output ngrok-v3.tgz

Extract the file:
tar -xvzf ngrok-v3.tgz

Authenticate ngrok: Sign up for a free account at ngrok.com to get your authtoken.
```

### Replace <YOUR_NGROK_AUTHTOKEN> with the token from your ngrok dashboard

./ngrok config add-authtoken <YOUR_NGROK_AUTHTOKEN>
Running ngrok for Demonstration
Start the Flask Server in Terminal 1 (as described in the daily workflow).

In a second terminal, start the ngrok tunnel:

```bash
./ngrok http 5000
Copy the public https URL provided by ngrok (it will look like https://random-string.ngrok-free.app).

Open your browser and navigate to that URL, adding /apidocs to the end.

Example: https://your-ngrok-url.ngrok-free.app/apidocs
```
This will load the full, interactive Swagger UI documentation for all API endpoints.

## Copyright & License

© 2025 Kgotso Mphuthi. All Rights Reserved.

This software is the proprietary property of Kgotso Mphuthi. You are granted temporary permission to view the source code for the sole purpose of assessing my technical skills. No other rights are granted. You may not copy, modify, distribute, or use this software for any other purpose without my express written permission.

---

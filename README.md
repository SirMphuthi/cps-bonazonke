# Community Protection Service (CPS) #BONAZONKE

### Developed by Kgotso Mphuthi

## 1. Project Overview

Welcome to my web stack portfolio project. For this project, I developed the **Community Protection Service (CPS)**, a backend framework designed to tackle the real-world problem of slow emergency response times in urban areas.

My goal was to design and build a robust, secure, and scalable system that could serve as the core logic for a network of automated surveillance drones and coordinated ground units. The system manages incident reports, identifies available assets, simulates a flight clearance process, and secures its endpoints using token-based authentication. This project demonstrates my ability to architect a complete backend solution from the ground up.

## 2. Technology Choices & Architecture

I carefully selected the following technologies to build a modern and professional application, keeping flexibility, reliability, and professional standards in mind.

* **Language: Python** & **Framework: Flask**
    * **Why:** I chose Flask for its flexibility, which allowed me to design a custom architecture from scratch and implement professional patterns like application factories and service layers.

* **Database Engine: SQLite**
    * **Why:** For this development build, I chose SQLite because it is a simple, serverless, file-based database engine that is incredibly easy to set up and manage, making the project highly portable and easy for anyone to run.

* **ORM: Flask-SQLAlchemy & Flask-Migrate**
    * **Why:** I used SQLAlchemy to interact with the SQLite database in a more Pythonic way. This abstracts away the raw SQL and allows the same application code to work with other databases like PostgreSQL with minimal changes. To manage the database schema safely, I integrated Flask-Migrate.

* **Security: Flask-JWT-Extended**
    * **Why:** To secure the API, I implemented JSON Web Tokens (JWT), the industry standard for stateless authentication in modern web services.

* **API Documentation: Flasgger**
    * **Why:** Clear documentation is essential. I implemented Flasgger to auto-generate a live, interactive Swagger UI page, making my API easily understandable and testable.

My architectural approach also plans for future growth by separating concerns, allowing for complex features like image analysis to be built out as independent microservices.

---

## 3. Local Setup and Installation

To get the project running on your local machine, you will need Python 3.8+.

#### Step 1: Clone the Repository
*(Fork the repository to your own GitHub first)*
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

#### Step 3: Configure Environment Variables
Create your local `.env` file by copying the template.
```bash
cp .env.example .env
```
*(The default configuration in this file is already set up to use the local SQLite database.)*

---

## 4. Database Initialization

Before running the app, you must create the database file and its tables.

1.  **Initialize the migrations folder** (only run this once per project):
    ```bash
    flask db init
    ```
2.  **Generate the migration script based on the models:**
    ```bash
    flask db migrate -m "Initial database schema"
    ```
3.  **Apply the migrations to create the tables:**
    ```bash
    flask db upgrade
    ```
4.  **(Recommended) Seed the database** with sample data for a clean demonstration:
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

## 6. How to Test the Secure API

Once the server is running, open a **second terminal** with the virtual environment activated (`source venv/bin/activate`). You must log in to get an access token before testing other features.

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
This will return an `access_token`. **Copy the long string of characters inside the quotes.**

### Step 2: Test a Protected Endpoint
Store the token in a shell variable and use it to access a protected route.
```bash
# Replace <COPIED_TOKEN> with the actual token you copied
TOKEN="<COPIED_TOKEN>"

# Now, use the token to get the list of drones
curl [http://127.0.0.1:5000/api/drones](http://127.0.0.1:5000/api/drones) -H "Authorization: Bearer $TOKEN"
```
This workflow of logging in and using the returned token is how modern, secure APIs are tested.

---

## 7. Interactive API Documentation

For a more user-friendly way to explore the API, an interactive Swagger UI page is automatically generated.

* **How to access:** While the Flask server is running, open your web browser and navigate to:
    **`http://127.0.0.1:5000/apidocs`**

---

## Copyright & License

© 2025 Kgotso Mphuthi. All Rights Reserved.

This software is the proprietary property of Kgotso Mphuthi. You are granted temporary permission to view the source code for the sole purpose of assessing my technical skills. No other rights are granted. You may not copy, modify, distribute, or use this software for any other purpose without my express written permission.

---

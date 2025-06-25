# Community Protection Service (CPS) #BONAZONKE

### Developed by Kgotso Mphuthi

## 1. Project Overview

Welcome to my web stack portfolio project. For this project, I developed the **Community Protection Service (CPS)**, a backend framework designed to tackle the real-world problem of slow emergency response times in urban areas.

My goal was to design and build a robust, secure, and scalable system that could serve as the core logic for a network of automated surveillance drones. The system manages incident reports, identifies available drones, simulates a flight clearance process, and secures its endpoints using token-based authentication. This project demonstrates my ability to architect a complete backend solution from the ground up to solve a complex problem.

## 2. Technology Choices & Architecture

I carefully selected the following technologies to build a modern and professional application.

* **Language: Python** & **Framework: Flask**
    * **Why:** I chose Flask for its flexibility, which allowed me to design a custom architecture from scratch and implement professional patterns like application factories and service layers.

* **Database: PostgreSQL / SQLite**
    * **Why:** The application is designed to use PostgreSQL for its robustness and data integrity in a production-like environment. For simplicity in development and demonstration, it is configured to use SQLite, showcasing its adaptability to different database backends.

* **ORM: Flask-SQLAlchemy & Flask-Migrate**
    * **Why:** I used SQLAlchemy to interact with the database in a more Pythonic way. To manage changes to the database schema safely as the models evolved, I integrated Flask-Migrate.

* **Security: Flask-JWT-Extended**
    * **Why:** To secure the API, I implemented JSON Web Tokens (JWT), the industry standard for stateless authentication in modern web services. This ensures that data can only be accessed by authorized users.

* **API Documentation: Flasgger**
    * **Why:** Clear documentation is essential. I implemented Flasgger to auto-generate a live, interactive Swagger UI page, making my API easily understandable and testable.

---

## 3. Local Setup and Installation

To get the project running on your local machine, you will need Python 3.8+ and the necessary build tools.

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
*(Note: If the above command fails on a fresh system, you may need to install system-level development tools first with `sudo apt-get install postgresql libpq-dev`)*

#### Step 3: Configure Environment Variables
Create your local `.env` file by copying the template. This file tells the application how to connect to the database and what secret keys to use.
```bash
cp .env.example .env
```
*(The default configuration is set up to use a local SQLite database file, which requires no extra setup.)*

---

## 4. Database Initialization

Before running the app, you must create the database file and its tables.

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
4.  **(Recommended) Seed the database** with sample data for a clean demonstration. This script will wipe existing data first.
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

Once the server is running, open a **second terminal** with the virtual environment activated (`source venv/bin/activate`). Since the API is now secure, you must log in to get an access token before you can test other features.

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

Now, you can use that token to access any protected route. We will store it in a shell variable for convenience.

```bash
# Replace <COPIED_TOKEN> with the actual token you copied
TOKEN="<COPIED_TOKEN>"

# Now, use the token to get the list of drones
curl [http://127.0.0.1:5000/api/drones](http://127.0.0.1:5000/api/drones) -H "Authorization: Bearer $TOKEN"
```
This workflow of logging in and using the returned token is how modern, secure APIs are tested and used.

---

## 7. Interactive API Documentation

For a more user-friendly way to explore the API, I have integrated Flasgger to provide a live Swagger UI documentation page.

* **How to access:** While the Flask server is running, open your web browser and navigate to:
    **`http://127.0.0.1:5000/apidocs`**

---

## Copyright & License

© 2025 Kgotso Mphuthi. All Rights Reserved.

This software is the proprietary property of Kgotso Mphuthi. You are granted temporary permission to view the source code for the sole purpose of assessing my technical skills. No other rights are granted. You may not copy, modify, distribute, or use this software for any other purpose without my express written permission.

---

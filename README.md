
# Community Protection Service (CPS) #BONAZONKE

### Developed by Kgotso Mphuthi

---

## 1. Project Overview

Community Protection Service (CPS) is a real-world emergency response and analytics platform designed for urban communities. Originally a portfolio project, CPS is now being developed for production use, with a focus on robust backend services, a user-friendly dashboard, and desktop application support.

The system coordinates automated surveillance drones and ground units, providing both reactive incident response and proactive crime hotspot analysis. CPS is now evolving to include live data integration (e.g., weather) and a desktop app powered by Electron for seamless daily use.


## 2. Features

- **Intelligent Asset Dispatch:** Geospatial calculations (`geopy`) to dispatch the closest drone to incidents.
- **Predictive Hotspot Analysis:** Analytics endpoint for identifying high-density crime zones.
- **Secure, Token-Based Authentication:** All APIs protected with JWT.
- **Third-Party Integration:** Simulated Air Traffic Control (ATC) service integration.
- **Comprehensive Data Modeling:** Relational database with migrations.
- **Live Data Integration:** (Planned) Real-time weather data displayed on the dashboard via public APIs.
- **Desktop Application:** (Planned) Electron-based desktop app for easy access and daily workflow.


## 3. Technology Stack & Architecture

- **Backend:** Python (Flask), Flask-SQLAlchemy, Flask-Migrate, Flask-JWT-Extended
- **Frontend:** HTML/CSS/JS (Jinja2 templates), planned Electron desktop app
- **Database:** SQLite (development), PostgreSQL/MySQL (recommended for production)
- **Geospatial:** geopy
- **API Docs:** Flasgger (Swagger)
- **Live Data:** Integration with public APIs (e.g., OpenWeatherMap)
- **Containerization:** Docker, Docker Compose
- **Deployment:** Cloud-ready, CI/CD recommended

---

## 4. Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js & npm (for Electron app)
- Docker (optional, for containerized deployment)

### Clone the Repository
```bash
git clone https://github.com/SirMphuthi/cps-bonazonke.git
cd cps-bonazonke
```

### Environment Variables
Copy `.env.example` to `.env` and update with your secrets/configs.
```bash
cp .env.example .env
```

### Backend Setup (Windows/Linux)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
flask db upgrade
python seed.py  # Optional: seed database
flask run --host=0.0.0.0
```

### Electron Desktop App (Planned)
Instructions for building and running the Electron app will be added once implemented.

### Docker Setup
```bash
docker-compose up --build
```
    ```



---


## 5. Usage

### Running the Backend
Follow the setup instructions above. Access the dashboard at `http://127.0.0.1:5000/`.

### API Authentication
Log in via `/api/login` to obtain a JWT token. Use this token to access protected endpoints.

### Example: Get Crime Hotspots
```bash
curl -X POST http://127.0.0.1:5000/api/login \
-H "Content-Type: application/json" \
-d '{"username": "operator1", "password": "password123"}'

# Use the returned token:
curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:5000/api/analytics/hotspots
```


### Live Weather Data (Planned)
The dashboard will soon display live weather data using public APIs. Stay tuned for updates.

### Electron Desktop App (Planned)
You will be able to launch CPS as a desktop application for daily use. Instructions will be added after implementation.

### ngrok (Development Only)
ngrok is recommended for development, demos, and remote testing when your environment blocks localhost or you need to share your local server externally. It is not suitable for production deployment.

To use ngrok for development:
```bash
curl -L https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz --output ngrok-v3.tgz
tar -xvzf ngrok-v3.tgz
./ngrok http 5000
```
Copy the public URL provided by ngrok and use it to access your local server remotely.

For production, deploy your backend to a cloud provider or VPS with a public IP/domain and proper SSL setup.


## 6. API Documentation

Interactive Swagger UI is available at `/apidocs` when the backend is running. For remote access during development, use ngrok. For production, deploy to a cloud provider and configure public access securely.


## 7. Deployment

- **Docker:** Use `docker-compose up --build` for local or server deployment.
- **Cloud:** Prepare environment variables and production database. Recommended providers: AWS, Azure, GCP.
- **Electron Packaging:** (Planned) Desktop app will be packaged for Windows/Mac/Linux.

## 8. Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

## 9. License

© 2025 Kgotso Mphuthi. All Rights Reserved.

This software is the proprietary property of Kgotso Mphuthi. You are granted temporary permission to view the source code for the sole purpose of assessing my technical skills. No other rights are granted. You may not copy, modify, distribute, or use this software for any other purpose without express written permission.

---

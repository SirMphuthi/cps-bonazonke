# run.py
from app import create_app, db
from pyngrok import ngrok
import os

# Create the Flask app instance
app = create_app()

# This block runs only when the script is executed directly
if __name__ == '__main__':
    # The 'with app.app_context()' ensures that the application
    # context is available for database operations.
    with app.app_context():
        db.create_all()

    # --- Ngrok Tunnel Setup ---
    # Get the ngrok authtoken from your .env file
    authtoken = os.environ.get("NGROK_AUTHTOKEN")
    if authtoken:
        ngrok.set_auth_token(authtoken)
    else:
        print("!!! Ngrok authtoken not found. Please add it to your .env file. !!!")

    # Start an HTTP tunnel on port 5000
    public_url = ngrok.connect(5000)
    print("====================================================================")
    print(f" * YOUR LIVE DASHBOARD IS RUNNING ON: {public_url}")
    print("====================================================================")

    # Start the Flask development server
    app.run(port=5000)

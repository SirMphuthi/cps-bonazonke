# debug_db.py
import os
from dotenv import load_dotenv

print("--- Starting Database Debug ---")

# Load the .env file
load_dotenv()
print("Loaded .env file.")

# Get the database URL from the environment
db_url = os.getenv('DATABASE_URL')

print(f"\n[INFO] The DATABASE_URL from your .env file is:")
print(f"--> {db_url}\n")

# Check if it's a SQLite path
if db_url and db_url.startswith('sqlite:///'):
    # Get the path part of the URL
    path_part = db_url.replace('sqlite:///', '')
    
    # If it's a relative path, resolve its absolute path
    if not path_part.startswith('/'):
        absolute_path = os.path.abspath(path_part)
        print("[INFO] This is a relative path. The absolute file path your app is using is:")
        print(f"--> {absolute_path}\n")
    else:
        print("[INFO] This is an absolute path.")

print("--- End of Debug ---")

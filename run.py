import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
dotenv_path = os.path.join(BASE_DIR, ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print("WARNING: .env file not found at", dotenv_path)


from app import create_app

app = create_app(os.getenv("FLASK_CONFIG") or "dev")

if __name__ == "__main__":
    app.run()
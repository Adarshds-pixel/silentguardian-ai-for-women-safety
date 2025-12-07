import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:8501")

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")  # optional

# Models
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "small")

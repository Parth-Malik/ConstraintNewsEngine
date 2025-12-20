import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # --- API KEYS ---
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")

    # FIX: Read 'GROQ_API_KEY' from .env (since that is what you named it)
    _groq_keys_raw = os.getenv("GROQ_API_KEY", "")

    # Split the comma-separated string into a list
    GROQ_API_KEYS = [key.strip() for key in _groq_keys_raw.split(",") if key.strip()]

    # Fallback for single key usage
    GROQ_API_KEY = GROQ_API_KEYS[0] if GROQ_API_KEYS else None

    # --- MODELS ---
    MODEL_REASONING = "llama-3.3-70b-versatile"
    MODEL_SUMMARY = "llama-3.1-8b-instant"
    MAX_ARTICLES = 5
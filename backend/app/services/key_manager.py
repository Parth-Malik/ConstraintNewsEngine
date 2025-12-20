from backend.config import Config


# --- GROQ KEY MANAGER (Existing) ---
class GroqKeyManager:
    def __init__(self):
        self.keys = getattr(Config, "GROQ_API_KEYS", [])
        # Fallback for legacy single key
        if not self.keys and getattr(Config, "GROQ_API_KEY", None):
            self.keys = [Config.GROQ_API_KEY]
        self.current_index = 0

    def get_active_key(self):
        if not self.keys:
            return None
        return self.keys[self.current_index]

    def switch_key(self):
        if not self.keys:
            return None
        self.current_index = (self.current_index + 1) % len(self.keys)
        print(f"🔄 [Groq] Rate Limit Hit. Switching to Key #{self.current_index + 1}...")
        return self.keys[self.current_index]


# --- NEWSAPI KEY MANAGER (New) ---
class NewsKeyManager:
    def __init__(self):
        # Handle both single string and comma-separated string from Config
        raw_keys = getattr(Config, "NEWS_API_KEY", "")
        self.keys = []

        if raw_keys:
            # Split by comma if it's a string containing multiple keys
            self.keys = [k.strip() for k in raw_keys.split(",") if k.strip()]

        self.current_index = 0

    def get_active_key(self):
        if not self.keys:
            print("❌ [KeyManager] Critical Error: No NewsAPI Keys configured!")
            return None
        return self.keys[self.current_index]

    def switch_key(self):
        if not self.keys:
            return None
        self.current_index = (self.current_index + 1) % len(self.keys)
        print(f"🔄 [NewsAPI] Limit Hit. Switching to Key #{self.current_index + 1}...")
        return self.keys[self.current_index]


# --- GLOBAL INSTANCES ---
groq_keys = GroqKeyManager()
news_keys = NewsKeyManager()  # Import this into ingestion.py
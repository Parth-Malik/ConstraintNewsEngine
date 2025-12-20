from groq import Groq
from backend.config import Config
# IMPORT THE SHARED MANAGER (Crucial for sync)
from backend.app.services.key_manager import groq_keys


class NewsCompressor:
    def __init__(self):
        # Initialize with the global active key from the shared manager
        self.client = Groq(api_key=groq_keys.get_active_key())

    def generate_summary(self, title, facts):
        if not facts:
            return "Intelligence gathering in progress. Detailed facts are currently unavailable for this specific report."

        # Ensure the client always has the fresh key (in case Extraction rotated it)
        self.client = Groq(api_key=groq_keys.get_active_key())

        try:
            # --- YOUR EXACT PROMPT (UNCHANGED) ---
            prompt = f"""
            Headline: {title}
            Facts: {str(facts)}

            Task: Write a professional, comprehensive news summary.
            Constraints:
            1. Length: Exactly 70 to 80 words.
            2. Tone: Journalistic and objective.
            3. Requirement: Flow logically; do not just list the facts.
            4. Focus: Stay strictly on the headline context.
            """

            res = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=Config.MODEL_SUMMARY
            )
            return res.choices[0].message.content.strip()

        except Exception as e:
            # --- RATE LIMIT HANDLING ---
            if "429" in str(e):
                print(f"⚠️ Summary Limit Hit! Requesting Global Rotation...")
                # Rotate the key globally (Extraction will see this change too)
                groq_keys.switch_key()

                # Recursive retry with the new key
                return self.generate_summary(title, facts)

            # --- STANDARD ERROR HANDLING ---
            print(f"❌ Summary Error: {e}")
            return "Summary generation encountered a temporary synchronization error."
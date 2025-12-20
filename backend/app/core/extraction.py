import json
from groq import Groq
from backend.config import Config
# IMPORT THE SHARED MANAGER (Crucial for sync)
from backend.app.services.key_manager import groq_keys

class FactExtractor:
    def __init__(self):
        # Initialize client with the current active key from the shared manager
        self.client = Groq(api_key=groq_keys.get_active_key())

    def extract_facts(self, article_text, target_topic=None):
        """
        Extracts exactly 2 key facts ONLY IF the article matches the target_topic.
        Includes automatic API key rotation on 429 errors.
        """
        try:
            # Re-instantiate to ensure we use the global active key
            self.client = Groq(api_key=groq_keys.get_active_key())

            # 1. INTELLIGENCE INJECTION: Create a topic-aware system prompt
            # This prevents "Cricket" searches from returning "Nintendo" news
            topic_constraint = ""
            if target_topic and target_topic.lower() != "all":
                topic_constraint = (
                    f"CRITICAL: First, verify if this text is related to '{target_topic}'. "
                    f"If the text is UNRELATED to '{target_topic}', return {{\"facts\": []}}. "
                )

            system_prompt = (
                "You are a precision neural news extraction engine. Output ONLY valid JSON. "
                f"{topic_constraint}"
                "Extract exactly 2 key facts from the provided text. Use this exact flat structure:\n"
                "{\"facts\": [{\"actor\": \"...\", \"action\": \"...\", \"object\": \"...\"}]}"
            )

            user_content = (
                f"Extract 2 key facts from this article: '''{article_text[:3000]}'''\n"
                "Requirements: Output valid JSON, no extra fields, 2 facts only. "
                "If the text is irrelevant to the search intent, return an empty facts list."
            )

            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                model="llama-3.1-8b-instant",
                response_format={"type": "json_object"},
                temperature=0.1 # Low temperature for high precision
            )

            data = json.loads(response.choices[0].message.content)
            facts = data.get("facts", [])

            # 2. VALIDATION: Ensure we only return facts that actually have content
            valid_facts = [f for f in facts if f.get("actor") and f.get("action")][:2]
            
            if not valid_facts:
                print(f"🔎 [Extraction] Intelligence Guard: Article rejected as irrelevant to '{target_topic}'")
            
            return valid_facts

        except Exception as e:
            # Handle Rate Limit (429) specifically
            if "429" in str(e):
                print(f"⚠️ Extraction Limit Hit! Requesting Global Rotation...")
                groq_keys.switch_key()
                # Recursive retry with the new key
                return self.extract_facts(article_text, target_topic)

            elif "400" in str(e):
                print(f"   ❌ API Logic Error: {e}")
            else:
                print(f"   ❌ Extraction Error: {e}")
            return []
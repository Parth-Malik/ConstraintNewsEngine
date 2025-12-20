import requests
import sys
import os
from bs4 import BeautifulSoup
from backend.config import Config
from backend.app.services.key_manager import news_keys


class NewsIngestor:
    def fetch_articles(self, query=None, category=None, page=1):
        # 1. Get Active Key
        current_key = news_keys.get_active_key()
        if not current_key:
            return []

        # 2. DEFAULT SETTINGS (Top Headlines)
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": current_key,
            "page": page,
            "pageSize": 10,
            "language": "en"
        }

        # Flags to track our mode
        target_country = "us"  # Default to US
        use_everything_endpoint = False

        # 3. ROBUSTNESS LOGIC: Detect "Live" intent
        if query:
            keywords = ["live", "score", "vs", "match", "result", "winner", "today"]
            if any(k in query.lower() for k in keywords):
                use_everything_endpoint = True  # "Live" needs recency, so we use /everything

        # 4. CATEGORY MAPPING
        if category:
            cat_lower = category.lower()

            # Case A: INDIA -> Switch country, keep Top Headlines
            if cat_lower == "india":
                target_country = "in"
                params["category"] = "general"

            # Case B: POLITICS -> Not a standard category, must use Search
            elif cat_lower == "politics":
                use_everything_endpoint = True
                params["q"] = "politics"
                params["sortBy"] = "publishedAt"

            # Case C: WORLD -> Just US General headlines
            elif cat_lower == "world":
                target_country = "us"
                params["category"] = "general"

            # Case D: STANDARD CATEGORIES (Health, Sports, etc.)
            elif cat_lower != "all":
                params["category"] = cat_lower

        # 5. QUERY HANDLING (Overrides Category logic)
        if query:
            use_everything_endpoint = True
            params["q"] = query
            params["sortBy"] = "publishedAt" if query and "live" in query.lower() else "relevancy"

        # 6. FINALIZE PARAMS BASED ON ENDPOINT
        if use_everything_endpoint:
            url = "https://newsapi.org/v2/everything"
            # CRITICAL FIX: The /everything endpoint HATES the 'country' and 'category' params.
            # We must ensure they are NOT in the params dict.
            params.pop("country", None)
            params.pop("category", None)
        else:
            # We are using /top-headlines, so we MUST have country (and optional category)
            params["country"] = target_country

        # 7. EXECUTE REQUEST
        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("status") == "error":
                code = data.get("code")
                # Handle Rate Limits by rotating keys
                if code in ["rateLimited", "apiKeyExhausted"]:
                    news_keys.switch_key()
                    return self.fetch_articles(query, category, page)

                print(f"   ❌ NewsAPI Error: {data.get('message')}")
                return []

            return data.get("articles", [])

        except Exception as e:
            print(f"   ❌ Ingestion Error: {e}")
            return []

    def scrape_full_content(self, url):
        """ Scrapes article text. Unchanged. """
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            res = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            for script in soup(["script", "style", "nav", "footer", "iframe"]):
                script.decompose()
            text = soup.get_text(separator=' ')
            clean_text = ' '.join(text.split())
            return clean_text[:5000]
        except:
            return ""
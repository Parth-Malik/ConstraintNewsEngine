import sys
import os
import json
from flask import Blueprint, request, jsonify

# 1. Define the Blueprint
api_bp = Blueprint('api', __name__)

# 2. Path Fix: Ensure the backend root is in the searchable path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

# 3. Import the LangGraph Agent
try:
    from app.workflows.graph import app as sigma_agent
except ImportError:
    from backend.app.workflows.graph import app as sigma_agent


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Service status check."""
    return jsonify({
        "status": "healthy",
        "service": "Sigma Intelligence Engine",
        "version": "2.1.0"
    })


@api_bp.route('/feed', methods=['GET'])
def get_news_feed():
    """
    Primary data endpoint for Categories and Search.
    Orchestrates the multi-key AI pipeline via LangGraph.
    """
    category = request.args.get('category', 'all')
    query = request.args.get('query', '')
    page = int(request.args.get('page', 1))

    # Determine mode to prevent NameError
    current_mode = "search" if query else "feed"

    # 🔒 NORMALIZATION (PRESERVED)
    normalized_category = category.strip().lower()

    # --- 🇮🇳 INDIA SPECIAL CASE: BOOSTED SEARCH INTENT ---
    # We only modify the 'search_intent' for India to ensure the scraper finds data.
    # Logic for every other category and search remain untouched.
    search_intent = query
    if not query and normalized_category == "india":
        # Broaden keywords specifically for the India category
        search_intent = "India national news breaking national"
    elif not query:
        search_intent = category

    print(f"\n📡 [API] Fetching {search_intent} | Mode: {current_mode} | Page: {page}")

    try:
        # Use the boosted search_intent to provide the agent with high-relevance data
        if normalized_category == "india" and not query:
            inputs = {
                "query": search_intent, # Boosted keywords
                "category": "india",
                "page": page,
                "mode": "feed",
                "raw_articles": [],
                "feed_items": []
            }
        else:
            inputs = {
                "query": query,
                "category": category,
                "page": page,
                "mode": current_mode,
                "raw_articles": [],
                "feed_items": []
            }

        # The agent nodes (Extraction/Compression) Sam logic (PRESERVED)
        result = sigma_agent.invoke(inputs)

        return jsonify({
            "feed": result.get("feed_items", []),
            "status": "success",
            "page": page,
            "mode": inputs["mode"]
        })

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "limit reached" in error_msg.lower():
            print("🛑 [CRITICAL] All Groq API Keys have reached their limits.")
            return jsonify({
                "error": "Intelligence capacity reached for the day.",
                "code": "LIMIT_EXHAUSTED"
            }), 429

        print(f"❌ [API Error]: {error_msg}")
        return jsonify({"error": "Internal synchronization error."}), 500


@api_bp.route('/analyze', methods=['POST'])
def run_analysis():
    """Legacy endpoint for backward compatibility (PRESERVED)."""
    data = request.json
    topic = data.get("topic", "Global Intelligence")

    try:
        inputs = {
            "query": topic,
            "category": "",
            "page": 1,
            "mode": "search",
            "raw_articles": [],
            "feed_items": []
        }
        result = sigma_agent.invoke(inputs)

        return jsonify({
            "feed": result.get("feed_items", []),
            "status": "success"
        })
    except Exception as e:
        print(f"❌ [Analysis Error]: {e}")
        return jsonify({"error": "Failed to process deep analysis."}), 500
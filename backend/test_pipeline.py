import sys
import os
import json
import time

# --- PATH SETUP (CRITICAL FIX) ---
# We point 1 level up ("..") so Python sees 'ConstraintNewsEngine-main' as the root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --- IMPORTS (FIXED FOR 'CORE' FOLDER) ---
# Your files are inside backend/app/core/, so we must include .core in the path
from backend.app.core.ingestion import NewsIngestor
from backend.app.core.clustering import NewsClustertizer
from backend.app.core.extraction import FactExtractor
from backend.app.core.compression import NewsCompressor
from backend.app.services.key_manager import groq_keys, news_keys


def run_system_check():
    print("\n🚀 STARTING SIGMA ENGINE DIAGNOSTIC...")
    print("=" * 60)

    # 1. KEY CHECK
    print("\n🔑 CHECKING API KEYS:")
    news_key = news_keys.get_active_key()
    groq_key = groq_keys.get_active_key()

    if news_key:
        print(f"   ✅ NewsAPI Key Active: ...{news_key[-5:]}")
    else:
        print("   ❌ NewsAPI Key MISSING (Check .env file)")
        return

    if groq_key:
        print(f"   ✅ Groq Key Active:    ...{groq_key[-5:]}")
    else:
        print("   ❌ Groq Key MISSING (Check .env file)")
        return

    # 2. INGESTION TEST
    print("\n📡 [Step 1] Testing INGESTION (Source: NewsAPI)...")
    ingestor = NewsIngestor()
    # Query 'Technology' to ensure we get results
    articles = ingestor.fetch_articles(category="technology", page=1)

    if not articles:
        print("   ❌ Ingestion Failed: No articles returned.")
        return

    print(f"   ✅ Successfully fetched {len(articles)} raw articles.")

    # Scrape just 2 articles to save time
    scraped_data = []
    print("   🕷️  Scraping content for top 2 articles...")
    for art in articles[:2]:
        content = ingestor.scrape_full_content(art['url'])
        if len(content) > 200:
            scraped_data.append({
                "title": art['title'],
                "description": art.get('description', ''),
                "content": content,
                "source": art['source']['name'],
                "url": art['url']
            })
            print(f"      - Scraped: {art['title'][:40]}...")

    if not scraped_data:
        print("   ❌ Scraping Failed: Could not extract text from URLs.")
        return

    # 3. CLUSTERING TEST
    print(f"\n🧩 [Step 2] Testing CLUSTERING on {len(scraped_data)} items...")
    clusterer = NewsClustertizer()
    clusters = clusterer.group_articles(scraped_data)
    unique_stories = clusterer.get_lead_articles(clusters)
    print(f"   ✅ Condensed into {len(unique_stories)} unique stories.")

    # 4. EXTRACTION & COMPRESSION TEST
    print("\n🧠 [Step 3 & 4] Testing AI PIPELINE (Targeting 1 Story)...")
    extractor = FactExtractor()
    compressor = NewsCompressor()

    target_story = unique_stories[0]
    print(f"   📄 Processing: '{target_story['title']}'")

    # A. Extraction
    try:
        print("      - Extracting Facts (Llama-3.1-8b)...")
        facts = extractor.extract_facts(target_story['content'])
        print(f"      ✅ Extraction Success! Found {len(facts)} facts.")
        print("      " + json.dumps(facts, indent=6).replace("\n", "\n      "))
    except Exception as e:
        print(f"      ❌ Extraction Error: {e}")
        return

    # B. Compression
    try:
        print("\n      - Generating Summary...")
        summary = compressor.generate_summary(target_story['title'], facts)
        print(f"      ✅ Summary Generated ({len(summary.split())} words):")
        print(f"      📢 \"{summary}\"")
    except Exception as e:
        print(f"      ❌ Summary Error: {e}")
        return

    print("\n" + "=" * 60)
    print("✅ DIAGNOSTIC COMPLETE: SYSTEM IS FULLY OPERATIONAL")
    print("=" * 60)


if __name__ == "__main__":
    run_system_check()
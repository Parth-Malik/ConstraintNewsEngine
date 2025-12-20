import sys
import os
import time
from typing import TypedDict, List, Literal

# --- PATH SETUP ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

# --- IMPORTS ---
from backend.app.core.ingestion import NewsIngestor
from backend.app.core.clustering import NewsClustertizer
from backend.app.core.extraction import FactExtractor
from backend.app.core.compression import NewsCompressor
from langgraph.graph import StateGraph, END


# --- 1. STATE DEFINITION ---
class AgentState(TypedDict):
    query: str
    category: str
    page: int
    mode: Literal["search", "feed"]
    raw_articles: List[dict]
    clustered_feed: List[dict]
    feed_items: List[dict]


# --- 2. NODE: SMART INGESTION (ROBUST FIX) ---
def node_ingest(state: AgentState):
    print(
        f"\n📡 [News Engine] Fetching {state['mode']} for '{state['query'] or state['category']}' (Page {state['page']})...")

    ingestor = NewsIngestor()

    articles = ingestor.fetch_articles(
        query=state["query"],
        category=state["category"],
        page=state["page"]
    )

    # Debug: See if API actually returned anything
    print(f"   🔎 API returned {len(articles)} raw headers. Scraping content...")

    processed = []
    limit = 15 if (state["category"] == "all" or state["mode"] == "search") else 10

    for art in articles[:limit]:
        # 1. Try to scrape the full live website
        scraped_text = ingestor.scrape_full_content(art["url"])

        # 2. FALLBACK LOGIC (The Fix):
        # If scraping failed (blocked) or text is too short, use the API description.
        # This ensures 'India' and 'World' news always show up.
        content = scraped_text
        if not content or len(content) < 150:
            # Combine description and API content snippet as a backup
            backup_text = f"{art.get('description', '')} {art.get('content', '')}"
            # Only use backup if it has some substance
            if len(backup_text) > 50:
                content = backup_text
            else:
                continue  # Skip only if we truly have ZERO text

        processed.append({
            "title": art.get("title"),
            "url": art.get("url"),
            "source": art.get("source", {}).get("name"),
            "image": art.get("urlToImage"),
            "content": content,
            "description": art.get("description", "")
        })

    return {"raw_articles": processed}


# --- 3. NODE: CLUSTERING ---
def node_cluster(state: AgentState):
    if not state["raw_articles"]:
        return {"clustered_feed": []}

    print(f"🧩 [Clustering] Grouping {len(state['raw_articles'])} raw articles...")

    clusterer = NewsClustertizer(similarity_threshold=0.45)
    clusters = clusterer.group_articles(state["raw_articles"])
    unique_stories = clusterer.get_lead_articles(clusters)

    print(f"   📉 Reduced to {len(unique_stories)} unique stories.")

    return {"clustered_feed": unique_stories}


# --- 4. NODE: FOCUSED PROCESSING ---
def node_process_feed(state: AgentState):
    items_to_process = state.get("clustered_feed", [])
    print(f"📰 [News Engine] Analyzing {len(items_to_process)} unique stories...")

    extractor = FactExtractor()
    compressor = NewsCompressor()

    final_feed = []

    for article in items_to_process:
        # 1. Extract Facts
        facts = extractor.extract_facts(article["content"])

        # 2. Generate Summary
        summary = compressor.generate_summary(article["title"], facts)

        final_feed.append({
            "title": article["title"],
            "summary": summary,
            "source": article["source"],
            "url": article["url"],
            "image": article["image"],
            "facts": facts
        })

    return {"feed_items": final_feed}


# --- 5. GRAPH CONSTRUCTION ---
workflow = StateGraph(AgentState)

workflow.add_node("ingest", node_ingest)
workflow.add_node("cluster", node_cluster)
workflow.add_node("process", node_process_feed)

workflow.set_entry_point("ingest")
workflow.add_edge("ingest", "cluster")
workflow.add_edge("cluster", "process")
workflow.add_edge("process", END)

app = workflow.compile()
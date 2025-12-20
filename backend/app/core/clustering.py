import sys
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering

# Fix path to ensure imports work correctly in the modular pipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))


class NewsClustertizer:
    def __init__(self, similarity_threshold=0.45):
        """
        threshold: How similar articles must be to group them (0 to 1).
        0.45 is usually the sweet spot for news headlines.
        """
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.threshold = similarity_threshold
        print("✅ [Clustering] Initialized (Local CPU mode - No API Keys needed)")

    def group_articles(self, articles):
        """
        Clusters a list of articles into distinct story groups using Bottom-Up Clustering.
        """
        if not articles or len(articles) < 2:
            return [[a] for a in articles]

        # 1. Combine titles and descriptions for a stronger comparison
        texts = [f"{a.get('title', '')} {a.get('description', '')}" for a in articles]

        # 2. Vectorize the text using TF-IDF (Term Frequency - Inverse Document Frequency)
        try:
            tfidf_matrix = self.vectorizer.fit_transform(texts)
        except ValueError:
            # Handle edge case where texts might be empty or stopwords only
            return [[a] for a in articles]

        # 3. Use Agglomerative Clustering
        # We use distance_threshold instead of n_clusters so the AI decides how many groups exist.
        clustering_model = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=1 - self.threshold,  # Distance = 1 - Similarity
            metric='cosine',
            linkage='average'
        )

        # 4. Perform the fit
        try:
            labels = clustering_model.fit_predict(tfidf_matrix.toarray())
        except Exception as e:
            print(f"⚠️ Clustering calculation failed: {e}. Returning raw list.")
            return [[a] for a in articles]

        # 5. Organize articles into their assigned groups
        clusters = {}
        for idx, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(articles[idx])

        # Return as a list of groups (e.g., [[story1_v1, story1_v2], [story2]])
        return list(clusters.values())

    def get_lead_articles(self, clusters):
        """
        Picks the best article from each cluster to show on the dashboard.
        """
        lead_items = []
        for group in clusters:
            # Logic: Prefer the article with the longest content (likely most informative)
            # If content length is missing, fallback to the first item.
            best_article = max(group, key=lambda x: len(x.get('content', '')))
            lead_items.append(best_article)

        return lead_items
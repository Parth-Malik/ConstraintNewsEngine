import sys
import os
from difflib import SequenceMatcher

# Fix path to ensure imports work correctly if run directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))


class ConflictResolver:
    def __init__(self):
        # Thresholds tailored for news headlines
        self.text_threshold = 0.5  # 50% character match
        self.overlap_threshold = 0.5  # 50% word overlap
        print("✅ [Conflict Resolver] Initialized (Local CPU mode - No API Keys needed)")

    def calculate_similarity(self, text1, text2):
        """Standard character matching (Levenshtein-ish)"""
        if not text1 or not text2:
            return 0.0
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def calculate_overlap(self, text1, text2):
        """
        Jaccard Similarity: Checks word overlap.
        Useful for: "SpaceX launched Starship" vs "SpaceX fired rocket"
        """
        set1 = set(text1.lower().split())
        set2 = set(text2.lower().split())

        if not set1 or not set2:
            return 0.0

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        return intersection / union if union > 0 else 0.0

    def find_agreements(self, facts_list_a, facts_list_b):
        """
        Compares two lists of facts to find agreements vs. unique info.
        """
        agreements = []
        unique_to_a = []

        # Make a copy to avoid modifying the original list during iteration
        remaining_b = facts_list_b.copy()

        for fact_a in facts_list_a:
            best_score = 0
            match_index = -1

            # Construct comparison sentence A
            sent_a = f"{fact_a.get('actor', '')} {fact_a.get('action', '')} {fact_a.get('object', '')}".strip()

            for idx, fact_b in enumerate(remaining_b):
                # Construct comparison sentence B
                sent_b = f"{fact_b.get('actor', '')} {fact_b.get('action', '')} {fact_b.get('object', '')}".strip()

                # Check 1: Strict Text Similarity
                sim_score = self.calculate_similarity(sent_a, sent_b)

                # Check 2: Word Overlap
                overlap_score = self.calculate_overlap(sent_a, sent_b)

                # We take the MAX of the two scores to be generous
                final_score = max(sim_score, overlap_score)

                if final_score > best_score:
                    best_score = final_score
                    match_index = idx

            # Decision Logic: Is it a match?
            if best_score >= self.text_threshold:
                agreements.append({
                    "fact": sent_a,
                    "confidence": "High (Multi-Source Agreement)",
                    "score": f"{best_score:.2f}"
                })
                # Remove matched fact from B so it doesn't get matched again
                if match_index >= 0:
                    remaining_b.pop(match_index)
            else:
                unique_to_a.append({
                    "fact": sent_a,
                    "confidence": "Medium (Single Source)"
                })

        return {"agreements": agreements, "unique_facts": unique_to_a}


# --- Quick Test Block (Runs only if executed directly) ---
if __name__ == "__main__":
    resolver = ConflictResolver()

    # Mock Data for testing
    source_cnn = [
        {"actor": "SpaceX", "action": "launched", "object": "Starship"},
        {"actor": "Musk", "action": "hailed", "object": "the landing"}
    ]
    source_bbc = [
        {"actor": "SpaceX", "action": "fired", "object": "Starship rocket"},
        {"actor": "NASA", "action": "praised", "object": "the mission"}
    ]

    result = resolver.find_agreements(source_cnn, source_bbc)

    print("\n✅ AGREED FACTS:")
    for item in result["agreements"]:
        print(f" - {item['fact']} (Score: {item['score']})")

    print("\n⚠️ UNIQUE FACTS:")
    for item in result["unique_facts"]:
        print(f" - {item['fact']}")
import json
import re

with open("fraud_keywords.json", "r", encoding="utf-8") as f:
    KEYWORDS = json.load(f)

WEIGHTS = {
    "high_risk": 30,
    "medium_risk": 15,
    "urgency": 10
}

def score_transcript(text):
    text_lower = text.lower()
    flagged = []
    raw_score = 0

    for tier, words in KEYWORDS.items():
        for word in words:
            # whole-word match, case insensitive
            pattern = r'\b' + re.escape(word.lower()) + r'\b'
            if re.search(pattern, text_lower):
                flagged.append({"word": word, "tier": tier})
                raw_score += WEIGHTS[tier]

    # cap at 100
    final_score = min(raw_score, 100)

    return {
        "score": final_score,
        "flagged": flagged,
        "flag_count": len(flagged)
    }
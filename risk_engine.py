from fraud_detector import score_transcript
from deepfake_detector import deepfake_score
from language_switch import detect_language_switches

WEIGHTS = {
    "keyword":  0.40,
    "deepfake": 0.35,
    "language": 0.10,
    "audio":    0.15
}

RISK_LEVELS = [
    (70, "CRITICAL", "🔴"),
    (55, "HIGH",     "🟠"),
    (30, "MEDIUM",   "🟡"),
    (0,  "LOW",      "🟢"),
]

def analyze_call(audio_path, transcript_roman, transcript_devanagari=""):
    combined_transcript = transcript_roman + " " + transcript_devanagari

    keyword_result  = score_transcript(combined_transcript)
    deepfake_result = deepfake_score(audio_path)
    language_result = detect_language_switches(transcript_roman)

    keyword_norm  = min(keyword_result["score"] / 100, 1.0)
    deepfake_norm = deepfake_result["deepfake_probability"]
    language_norm = language_result["switch_score"]

    final_score = (
        WEIGHTS["keyword"]  * keyword_norm  * 100 +
        WEIGHTS["deepfake"] * deepfake_norm * 100 +
        WEIGHTS["audio"]    * deepfake_norm * 100 +
        WEIGHTS["language"] * language_norm * 100
    )

    risk_level = "🟢 LOW"
    for threshold, label, emoji in RISK_LEVELS:
        if final_score >= threshold:
            risk_level = f"{emoji} {label}"
            break

    return {
        "final_score":       round(final_score, 1),
        "risk_level":        risk_level,
        "keyword_score":     keyword_result["score"],
        "keyword_flags":     keyword_result["flagged"],
        "deepfake_prob":     deepfake_result["deepfake_probability"],
        "is_ai_voice":       deepfake_result["is_ai_voice"],
        "language_switches": language_result["switches"],
        "switch_score":      language_result["switch_score"],
    }
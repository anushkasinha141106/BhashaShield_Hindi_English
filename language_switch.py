import re

HINDI_MARKERS = [
    "aapka", "aapko", "mein", "hai", "hoga", "karein", "karo",
    "abhi", "turant", "jaldi", "warna", "nahi", "agar", "aur",
    "se", "ko", "ka", "ki", "ke", "ho", "ja", "le", "de",
    "bata", "share", "band", "block", "freeze", "arrest",
    "main", "hoon", "aap", "yeh", "kya", "nahi", "mat",
    "jayega", "karenge", "milega", "rahega", "dena", "lena"
]

ENGLISH_MARKERS = [
    "your", "account", "suspended", "immediately", "please",
    "verify", "share", "click", "link", "details", "number",
    "update", "confirm", "urgent", "action", "required",
    "arrest", "cooperate", "freeze", "otp", "pin",
    "upi", "cvv", "aadhaar", "police", "legal", "court",
    "blocked", "call", "send", "now", "warning", "final"
]

def detect_language_switches(text):
    words = re.findall(r'\b\w+\b', text.lower())
    total = len(words)
    if total == 0:
        return {"switch_score": 0, "hindi_ratio": 0, "english_ratio": 0, "switches": 0}

    hindi_hits  = [w for w in words if w in HINDI_MARKERS]
    english_hits = [w for w in words if w in ENGLISH_MARKERS]

    hindi_ratio   = len(hindi_hits) / total
    english_ratio = len(english_hits) / total

    sequence = []
    for w in words:
        if w in HINDI_MARKERS:
            sequence.append("H")
        elif w in ENGLISH_MARKERS:
            sequence.append("E")

    switches = sum(1 for i in range(1, len(sequence)) if sequence[i] != sequence[i-1])
    switch_score = min(1.0, switches / 5)

    return {
        "switch_score":   round(switch_score, 3),
        "hindi_ratio":    round(hindi_ratio, 3),
        "english_ratio":  round(english_ratio, 3),
        "switches":       switches,
        "hindi_words":    hindi_hits,
        "english_words":  english_hits
    }
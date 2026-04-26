from fraud_detector import score_transcript

tests = [
    # --- fraud sentences (must score 50+) ---
    ("FRAUD", "Aapka account suspend ho jayega, abhi OTP share karo"),
    ("FRAUD", "Main CBI officer hoon, aapko arrest kiya jayega agar aap UPI pin nahi dete"),
    ("FRAUD", "Your account is blocked, please share your Aadhaar number immediately"),
    ("FRAUD", "10 minutes mein OTP send karo warna account freeze ho jayega"),
    ("FRAUD", "Turant apna CVV aur card number batao, legal action hogi"),

    # --- normal sentences (must score under 15) ---
    ("NORMAL", "Aaj mausam bahut accha hai, hum park mein jayenge"),
    ("NORMAL", "Mujhe kal subah meeting attend karni hai"),
    ("NORMAL", "Kya aap mujhe yeh form fill karne mein help karenge"),
    ("NORMAL", "Main apni dadi ke ghar ja raha hoon is weekend"),
    ("NORMAL", "Please mujhe grocery list bhej do jab time mile"),
]

print(f"{'Label':<8} {'Score':<7} {'Flags':<6} Text")
print("-" * 80)
for label, text in tests:
    result = score_transcript(text)
    status = "✓" if (label == "FRAUD" and result["score"] >= 50) or (label == "NORMAL" and result["score"] < 15) else "✗ FAIL"
    print(f"{label:<8} {result['score']:<7} {result['flag_count']:<6} {text[:50]}  {status}")
    if result["flagged"]:
        for f in result["flagged"]:
            print(f"         └─ [{f['tier']}] {f['word']}")
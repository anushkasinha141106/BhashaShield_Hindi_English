from language_switch import detect_language_switches

tests = [
    ("FRAUD", "Aapka account suspend ho jayega, please share your OTP immediately"),
    ("FRAUD", "Main CBI officer hoon, your account has been blocked, abhi verify karein"),
    ("FRAUD", "Turant apna UPI PIN share karo warna account freeze ho jayega"),
    ("NORMAL", "Aaj mausam bahut accha hai, hum park mein jayenge"),
    ("NORMAL", "Please send me the document by tomorrow morning"),
]

for label, text in tests:
    r = detect_language_switches(text)
    print(f"{label} | switches={r['switches']} score={r['switch_score']} | {text[:50]}")
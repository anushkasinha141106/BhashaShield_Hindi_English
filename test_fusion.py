from risk_engine import analyze_call, print_report

tests = [
    {
        "audio": "data/fake_voices/fake_001.wav",
        "transcript": "Aapka account suspend ho jayega, abhi OTP share karein",
        "expected": "HIGH or CRITICAL"
    },
    {
        "audio": "data/fake_voices/fake_005.wav", 
        "transcript": "Main CBI officer hoon, aapko arrest kiya jayega agar aap UPI pin nahi dete",
        "expected": "HIGH or CRITICAL"
    },
    {
        "audio": "data/real_voices/hin_0001.wav",
        "transcript": "Aaj mausam bahut accha hai, hum park mein jayenge",
        "expected": "LOW"
    },
    {
        "audio": "data/real_voices/hin_0002.wav",
        "transcript": "Mujhe kal subah meeting attend karni hai office mein",
        "expected": "LOW"
    },
]

for t in tests:
    print(f"Testing: {t['transcript'][:55]}...")
    print(f"Expected: {t['expected']}")
    result = analyze_call(t["audio"], t["transcript"])
    print_report(result)
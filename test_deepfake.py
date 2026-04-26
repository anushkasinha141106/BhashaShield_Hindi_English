import os
from deepfake_detector import deepfake_score

print("=== REAL VOICES (should score LOW < 0.5) ===")
real_files = [f for f in os.listdir("data/real_voices") if f.endswith(".wav")][:5]
for fname in real_files:
    result = deepfake_score(f"data/real_voices/{fname}")
    flag = "✓" if result["deepfake_probability"] < 0.5 else "✗ WRONG"
    print(f"{fname:<25} prob={result['deepfake_probability']}  pitch_var={result['pitch_variance']}  {flag}")

print("\n=== FAKE VOICES (should score HIGH > 0.5) ===")
fake_files = [f for f in os.listdir("data/fake_voices") if f.endswith(".wav")][:5]
for fname in fake_files:
    result = deepfake_score(f"data/fake_voices/{fname}")
    flag = "✓" if result["deepfake_probability"] > 0.5 else "✗ WRONG"
    print(f"{fname:<25} prob={result['deepfake_probability']}  pitch_var={result['pitch_variance']}  {flag}")
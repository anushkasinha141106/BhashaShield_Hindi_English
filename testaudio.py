import os
from audio_features import extract_features, simple_audio_score

# grab first 5 wav files automatically
voice_dir = "data/real_voices"
files = [f for f in os.listdir(voice_dir) if f.endswith(".wav")][:5]

print(f"{'File':<25} {'Pitch Variance':>15} {'Score':>7} {'Verdict'}")
print("-" * 65)

for fname in files:
    path = os.path.join(voice_dir, fname)
    result = simple_audio_score(path)
    print(f"{fname:<25} {result['pitch_variance']:>15.2f} {result['audio_score']:>7} {result['verdict']}")
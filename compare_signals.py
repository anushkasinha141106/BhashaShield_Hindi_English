import os
from deepfake_detector import deepfake_score

print(f"{'File':<25} {'prob':>6} {'pitch_var':>10} {'mfcc_var':>10} {'flatness':>10} {'embed_var':>12}")
print("-" * 80)

print("REAL:")
for fname in os.listdir("data/real_voices"):
    if fname.endswith(".wav"):
        r = deepfake_score(f"data/real_voices/{fname}")
        print(f"{fname:<25} {r['deepfake_probability']:>6} {r['pitch_variance']:>10} {r['mfcc_variance']:>10} {r['spectral_flatness']:>10} {r['embedding_variance']:>12}")

print("\nFAKE:")
for fname in os.listdir("data/fake_voices"):
    if fname.endswith(".wav"):
        r = deepfake_score(f"data/fake_voices/{fname}")
        print(f"{fname:<25} {r['deepfake_probability']:>6} {r['pitch_variance']:>10} {r['mfcc_variance']:>10} {r['spectral_flatness']:>10} {r['embedding_variance']:>12}")
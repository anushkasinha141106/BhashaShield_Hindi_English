# run this after generation: create_labels.py
import os
import csv

rows = []

for f in sorted(os.listdir("data/real_voices")):
    if f.endswith(".wav"):
        rows.append({"filename": f"real_voices/{f}", "label": 0, "type": "real"})

for f in sorted(os.listdir("data/fake_voices")):
    if f.endswith(".wav"):
        rows.append({"filename": f"fake_voices/{f}", "label": 1, "type": "fake"})

with open("data/labels.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["filename", "label", "type"])
    writer.writeheader()
    writer.writerows(rows)

print(f"labels.csv created with {len(rows)} entries")
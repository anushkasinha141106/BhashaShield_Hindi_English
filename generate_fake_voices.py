import requests
import os
import time
from fraud_scripts import FRAUD_SCRIPTS
from dotenv import load_dotenv
load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")  # or paste key directly
OUTPUT_DIR = "data/fake_voices"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_audio(text, filename):
    url = "https://api.sarvam.ai/text-to-speech"
    headers = {"api-subscription-key": SARVAM_API_KEY}
    payload = {
        "inputs": [text],
        "target_language_code": "hi-IN",
        "speaker": "anushka",       # Bulbul voice
        "pace": 1.0,
        "enable_preprocessing": True
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    if "audios" in result:
        import base64
        audio_data = base64.b64decode(result["audios"][0])
        with open(filename, "wb") as f:
            f.write(audio_data)
        return True
    else:
        print(f"ERROR on '{text[:40]}': {result}")
        return False

# Generate all 40
for i, script in enumerate(FRAUD_SCRIPTS):
    fname = os.path.join(OUTPUT_DIR, f"fake_{i+1:03d}.wav")
    
    if os.path.exists(fname):
        print(f"[{i+1}/40] Already exists, skipping")
        continue

    print(f"[{i+1}/40] Generating: {script[:50]}...")
    success = generate_audio(script, fname)
    
    if success:
        print(f"        Saved → {fname}")
    
    time.sleep(0.5)  # be nice to the API

print("\nDone! Counting files...")
count = len([f for f in os.listdir(OUTPUT_DIR) if f.endswith(".wav")])
print(f"fake_voices/ has {count} files")
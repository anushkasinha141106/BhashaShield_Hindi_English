from dotenv import load_dotenv
import requests
import os

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")  # or paste key directly for testing

def transcribe_hindi(wav_path):
    url = "https://api.sarvam.ai/speech-to-text"
    
    with open(wav_path, "rb") as f:
        files = {"file": (wav_path, f, "audio/wav")}
        headers = {"api-subscription-key": SARVAM_API_KEY}
        data = {
            "language_code": "hi-IN",
            "model": "saarika:v2.5"
        }
        response = requests.post(url, headers=headers, files=files, data=data)
    
    result = response.json()
    return result.get("transcript", "ERROR: " + str(result))

# Test it
transcript = transcribe_hindi("data/real_voices/hin_0001.wav")
print(transcript)
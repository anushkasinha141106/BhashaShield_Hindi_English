# BhashaShield

**Deepfake and Fraud Detection for Indian Regional Languages**

BhashaShield is a proof-of-concept audio analysis system that detects AI-generated (deepfake) voices and fraud intent in phone calls involving Indian regional languages. It processes a pre-recorded audio file and returns a unified risk score between 0 and 100, accompanied by a per-layer breakdown of the signals that contributed to the result.

The system is designed to address a gap that no existing consumer tool covers: simultaneous detection of voice spoofing and fraud semantics in code-mixed Hindi-English and Tamil-English speech.

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Detection Layers](#detection-layers)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Evaluation](#evaluation)
- [Limitations](#limitations)
- [References](#references)
- [Authors](#authors)

---

## Overview

Existing fraud detection tools such as TrueCaller rely on caller ID databases and are rendered ineffective when phone numbers are spoofed. Bank SMS alerts are post-facto and provide no real-time protection. No publicly available system analyses voice content for both AI-generation artefacts and fraud-intent signals in Indian languages simultaneously.

BhashaShield addresses three specific gaps:

1. No existing system combines deepfake detection with fraud keyword analysis for Indian language calls.
2. No existing system uses code-switching frequency as a behavioural fraud signal.
3. No labelled audio corpus exists for Hindi/Tamil fraud call detection.

This project was developed as Minor Project 1 for the B.Tech CSE programme (2024-2025) and submitted to the TrustAI Ideathon 2026 (Top 20 of 600+ teams).

---

## System Architecture

```
Input (.wav file)
        |
        v
Sarvam AI STT API  -->  Transcript
        |
        +---> Layer 1: AASIST Deepfake Detector       (weight: 0.35)
        |
        +---> Layer 2: Fraud Keyword Scoring Engine    (weight: 0.40)
        |
        +---> Layer 3a: Audio Heuristic Scorer         (weight: 0.15)
        |
        +---> Layer 3b: Language Switch Counter        (weight: 0.10)
                                    |
                                    v
                        Weighted Fusion Engine
                                    |
                                    v
                    Risk Score (0-100) + Explanation
```

**Fusion Formula**

```
Risk Score = (0.35 x deepfake_score)
           + (0.40 x keyword_score)
           + (0.15 x audio_heuristic_score)
           + (0.10 x language_switch_score)
```

| Score Range | Risk Level  |
|-------------|-------------|
| 0 - 30      | LOW RISK    |
| 31 - 69     | MEDIUM RISK |
| 70 - 100    | HIGH RISK   |

---

## Detection Layers

### Layer 1 — Deepfake Detection (35%)

Uses a pretrained AASIST-L model (Jung et al., ICASSP 2022) to analyse spectral and temporal artefacts in the audio waveform. Real human voices exhibit natural harmonic irregularities; AI-generated voices show unnatural smoothness. The SSL Anti-Spoofing Wav2Vec 2.0 model (Tak et al., Speaker Odyssey 2022) is used as a backup.

Neither model is trained from scratch. Both use publicly available pretrained checkpoints.

### Layer 2 — Fraud Keyword Scoring (40%)

A rule-based keyword engine scans the STT transcript for terms organised into three tiers:

- **High-risk:** OTP, PIN, CVV, Aadhaar, UPI, account number
- **Medium-risk:** suspended, blocked, CBI, RBI, police, arrested, legal action
- **Urgency markers:** turant, abhi, 10 minute mein, immediate, right now

Includes Hindi transliterations and English equivalents of all terms.

### Layer 3a — Audio Heuristic Scorer (15%)

Extracts low-level audio features using librosa: MFCCs (13 coefficients), spectral centroid, spectral rolloff, zero-crossing rate, RMS energy, and pitch variance. A low pitch variance relative to a calibrated threshold is treated as an AI-voice signal.

### Layer 3b — Language Switch Counter (10%)

Transcripts are chunked into 10-word windows. Each window is classified as predominantly Hindi or English using a dictionary-based heuristic. The number of language switches per minute is computed.

Natural Indian speakers switch languages 5 or more times per minute in conversational speech. Scripted fraud calls tend to remain in a single language. A low switch frequency in an otherwise suspicious call raises the final risk score.

This signal constitutes BhashaShield's primary original research contribution. No prior published work applies code-switching frequency as a fraud behavioural signal.

---

## Repository Structure

```
BhashaShield/
|
|-- SSL_Anti-spoofing/          # Submodule: Tak et al. pretrained Wav2Vec2 checkpoint
|
|-- app.py                      # Streamlit web application (main entry point)
|-- risk_engine.py              # Weighted fusion engine: analyze_call(audio_path)
|-- deepfake_detector.py        # AASIST wrapper: deepfake_score(audio_path)
|-- fraud_detector.py           # Keyword scoring: score_transcript(text)
|-- audio_features.py           # librosa feature extraction and heuristic scorer
|-- language_switch.py          # Code-switching frequency counter
|-- compare_signals.py          # Side-by-side signal comparison utility
|-- generate_fake_voices.py     # Sarvam Bulbul TTS batch generation script
|-- fraud_scripts.py            # 40 Hindi/English fraud script templates
|-- fraud_keywords.json         # Tiered keyword list (high/medium/urgency)
|-- create_labels.py            # Dataset labelling utility
|-- evaluate.py                 # Evaluation pipeline: F1, precision, recall, confusion matrix
|-- testsarvam.py               # Sarvam STT API connection test
|-- test_deepfake.py            # AASIST model smoke test
|-- test_fusion.py              # End-to-end fusion pipeline test
|-- test_language.py            # Language switch counter test
|-- testaudio.py                # Audio feature extractor test
|-- testkeywords.py             # Keyword engine unit test
|-- requirements.txt            # Python dependencies
|-- README.md
```

---

## Installation

**Prerequisites**

- Python 3.10 or higher
- pip
- A Sarvam AI account with an API key (free tier available at sarvam.ai)

**Steps**

```bash
# Clone the repository
git clone https://github.com/anushkasinha141106/BhashaShield.git
cd BhashaShield

# Install dependencies
pip install -r requirements.txt

# Download the AASIST pretrained checkpoint
# Follow instructions in SSL_Anti-spoofing/README.md

# Set your Sarvam API key as an environment variable
export SARVAM_API_KEY=your_key_here
```

**Key Dependencies**

```
openai-whisper
librosa
soundfile
transformers
torch
scikit-learn
streamlit
requests
noisereduce
```

---

## Usage

**Run the Streamlit demo application**

```bash
streamlit run app.py
```

Upload any `.wav` file through the browser interface. The application returns:

- Risk score (colour-coded: green / yellow / red)
- AI voice detection result (yes/no)
- Detected language
- Full transcript with fraud keywords highlighted
- Per-layer score breakdown (bar chart)

**Run analysis from Python**

```python
from risk_engine import analyze_call

result = analyze_call("path/to/audio.wav")

print(result["risk_score"])    # 0-100
print(result["risk_level"])    # LOW / MEDIUM / HIGH
print(result["transcript"])
print(result["detected_flags"])
print(result["breakdown"])
```

---

## Evaluation

The system was evaluated on a labelled dataset of 90 audio samples:

- 30 real voices sourced from Mozilla Common Voice (Hindi)
- 60 synthetic fraud voices generated using the Sarvam Bulbul TTS API

Evaluation metrics (sklearn.metrics):

| Metric    | Target |
|-----------|--------|
| Precision | > 0.70 |
| Recall    | > 0.70 |
| F1 Score  | > 0.70 |

Run the evaluation pipeline:

```bash
python evaluate.py
```

Output includes a confusion matrix saved as a PNG file and a per-sample results CSV.

**Note on dataset size:** The deep learning models (AASIST, Wav2Vec2) are not trained on this dataset. They use publicly available pretrained checkpoints. The 90 samples are used only to calibrate the fusion weights and measure system-level performance. The reported F1 score is therefore a lower bound; performance would improve with a larger and more diverse corpus.

---

## Limitations

| Limitation | Severity | Mitigation |
|---|---|---|
| Dataset limited to 90 samples | Medium | Pretrained models carry the detection load; 90 samples calibrate fusion weights only |
| No live call integration | High (product) / Low (research) | Pipeline latency under 500ms per 5-second chunk demonstrates real-time feasibility |
| Human scammers not caught by audio layer | Medium | Keyword layer (40% weight) catches fraud content regardless of voice origin |
| Coverage limited to Hindi, Tamil, English | Medium | Sarvam STT supports 22 Indian languages; keyword engine is extensible |
| Adversarial evasion possible | High (future risk) | Multi-signal ensemble raises cost of simultaneous evasion across all layers |
| Legitimate bank calls may trigger false positives | Low-Medium | Soft alerts with explainable output; whitelist integration planned |
| Noisy telephony degrades spectral analysis | Medium | noisereduce preprocessing; graceful fallback when SNR is too low |

---

## References

[1] J. Yamagishi et al., "ASVspoof 2021: Towards Spoofed and Deepfake Speech Detection in the Wild," *IEEE/ACM Trans. Audio, Speech, Lang. Process.*, 2022. arXiv:2210.02437.

[2] J. Jung et al., "AASIST: Audio Anti-Spoofing Using Integrated Spectro-Temporal Graph Attention Networks," *Proc. ICASSP 2022*. arXiv:2110.01200.

[3] H. Tak et al., "Automatic Speaker Verification Spoofing and Deepfake Detection Using Wav2Vec 2.0 and Data Augmentation," *Speaker Odyssey 2022*. GitHub: TakHemlata/SSL_Anti-spoofing.

[4] X. Li et al., "Cross-Domain Audio Deepfake Detection: Dataset and Analysis," arXiv:2404.04904, 2024.

[5] W. Ge et al., "A Data-Centric Approach to Generalizable Speech Deepfake Detection," arXiv:2512.18210, 2025.

[6] Y. A. Ghotekar et al., "Deepfake-Audio Detection for Indian Language," *IJERT*, Vol. 14, Iss. 12, 2025. DOI: 10.17577/IJERTV14IS120304.

[7] M. Chitale et al., "A Robust and Lightweight CNN-Transformer Model for Audio Deepfake Detection in Indian Languages," ResearchGate, 2024.

[8] Z. Ma et al., "TeleAntiFraud-28k: An Audio-Text Slow-Thinking Dataset for Telecom Fraud Detection," arXiv:2503.24115, 2025.

[9] Z. Shen et al., "It Warned Me Just at the Right Moment: Exploring LLM-based Real-Time Detection of Phone Scams," arXiv:2502.03964, 2025.

[10] T. Imam et al., "Multilingual Financial Fraud Detection Using Machine Learning and Transformer Models: A Bangla-English Study," arXiv:2603.11358, 2026.

[11] H. S. Chadha et al., "Code Switched and Code Mixed Speech Recognition for Indic Languages," arXiv:2203.16578, 2022.

[12] G. Winata et al., "The Decades Progress on Code-Switching Research in NLP: A Systematic Survey," *ACL Findings 2023*.

---

## Author
**Anushka Sujit Sinha** — B.Tech CSE, IIIT Pune (Student ID: 112415024)

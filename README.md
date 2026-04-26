# BhashaShield


BhashaShield is a multilingual AI-powered trust layer designed to help users identify potentially AI-generated or manipulated voice and text communication in real time.

The project is focused on detecting suspicious speech patterns, risky text behavior, and possible synthetic or cloned voices during live interactions.

Unlike traditional systems that detect fraud only after the damage is done, BhashaShield works during the interaction itself and provides a real-time trust score to help users make safer decisions.

Currently, the MVP supports:
- Hindi
- English
- Hinglish

Support for more Indian regional languages is planned in future versions.

Since Streamlit doesnt support live audio recordings, it couldnt be implemented in the deployed version.

---

## Problem Statement

AI-generated voices, cloned speech, and fake multilingual communication are becoming increasingly difficult to identify.

People often trust voices too easily, especially in stressful situations like:
- Banking calls
- Emergency situations
- OTP or payment requests
- Customer support scams
- Calls from unknown numbers
- Emotional manipulation in native languages

BhashaShield aims to reduce this risk by giving users live warnings and risk estimates instead of relying only on human judgement.

---

## Current MVP Scope

The current MVP is intentionally lightweight and focused on reliability.

### Supported Languages
- Hindi
- English
- Hinglish

### Supported Inputs
- Audio files
- Voice recordings
- Text messages
- Mixed-language communication

### Current Detection Layers
- Speech-to-text conversion
- Language detection
- Acoustic feature extraction
- Fraud keyword matching
- LLM-based suspicious conversation analysis
- Risk scoring engine

Even if certain APIs or external services fail, the system can still continue working using the fallback keyword detection system.

This ensures the MVP remains functional and resilient.

---

## Features(Still working on some points)

- Real-time voice and text analysis
- Hindi, English, and Hinglish support
- Automatic language identification
- Synthetic speech detection
- Keyword-based fraud detection
- LLM-assisted conversation analysis
- Weighted risk scoring system
- Real-time alert generation
- Human-in-the-loop decision support
- Fallback keyword detection even if APIs fail


---


## Project Structure

```bash
bhashashield_demo/
│── backend/
│   ├── .env
│   ├── audio_feature.py
│   ├── fraud_detector.py
│   ├── keywords.py
│   ├── llm_analysis.py
│   ├── stt.py
│   ├── utils.py
│
│── frontend/
│   ├── app.py
│
│── assets/
│── requirements.txt
│── README.md

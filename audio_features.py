import librosa
import numpy as np
import soundfile as sf

def extract_features(audio_path):
    y, sr = librosa.load(audio_path, sr=None)

    # 13 MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfccs, axis=1).tolist()

    # Spectral centroid
    centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))

    # Spectral rolloff
    rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))

    # Zero crossing rate
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))

    # RMS energy
    rms = np.mean(librosa.feature.rms(y=y))

    # Pitch variance — the key deepfake signal
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y, fmin=librosa.note_to_hz('C2'),
        fmax=librosa.note_to_hz('C7')
    )
    voiced_f0 = f0[voiced_flag]  # only use voiced frames
    pitch_variance = float(np.var(voiced_f0)) if len(voiced_f0) > 1 else 0.0

    return {
        "mfcc_mean": mfcc_mean,
        "spectral_centroid": float(centroid),
        "spectral_rolloff": float(rolloff),
        "zero_crossing_rate": float(zcr),
        "rms_energy": float(rms),
        "pitch_variance": float(pitch_variance)
    }


def simple_audio_score(audio_path, threshold=500.0):
    features = extract_features(audio_path)
    pv = features["pitch_variance"]

    if pv < threshold:
        # too smooth → suspicious → AI voice
        score = 60
    else:
        # natural variance → probably real
        score = 10

    return {
        "audio_score": score,
        "pitch_variance": pv,
        "verdict": "suspicious" if score == 60 else "likely_real"
    }
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HUGGINGFACE_HUB_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

import librosa
import numpy as np

def deepfake_score(audio_path):
    try:
        y, sr = librosa.load(audio_path, sr=16000)

        # Signal 1: Spectral flatness
        flatness = float(np.mean(librosa.feature.spectral_flatness(y=y)))

        # Signal 2: MFCC variance
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_var = float(np.mean(np.var(mfccs, axis=1)))

        # Signal 3: Spectral contrast
        contrast = float(np.mean(librosa.feature.spectral_contrast(y=y, sr=sr)))

        # Signal 4: Pitch variance using yin (fast version of pyin)
        f0 = librosa.yin(y, fmin=60, fmax=400)
        f0_voiced = f0[f0 > 0]
        pitch_var = float(np.var(f0_voiced)) if len(f0_voiced) > 1 else 0.0

        # Score flatness (strongest signal)
        if flatness < 0.012:
            flatness_score = 0.95
        elif flatness < 0.018:
            flatness_score = 0.60
        else:
            flatness_score = 0.10

        # Score MFCC
        if mfcc_var < 1200:
            mfcc_score = 0.85
        elif mfcc_var < 1500:
            mfcc_score = 0.55
        else:
            mfcc_score = 0.15

        # Score contrast
        if contrast > 30:
            contrast_score = 0.70
        elif contrast > 20:
            contrast_score = 0.40
        else:
            contrast_score = 0.15

        # Score pitch variance
        if pitch_var < 500:
            pitch_score = 0.80
        elif pitch_var < 2000:
            pitch_score = 0.50
        else:
            pitch_score = 0.10

        final = (
            0.50 * flatness_score +
            0.20 * mfcc_score +
            0.15 * pitch_score +
            0.15 * contrast_score
        )

        return {
            "deepfake_probability": round(final, 3),
            "is_ai_voice": final > 0.45,
            "spectral_flatness": round(flatness, 4),
            "mfcc_variance": round(mfcc_var, 2),
            "pitch_variance": round(pitch_var, 2),
            "spectral_contrast": round(contrast, 2),
            "method": "librosa_4signal"
        }

    except Exception as e:
        return {
            "deepfake_probability": 0.5,
            "is_ai_voice": False,
            "error": str(e),
            "method": "fallback_neutral"
        }
import streamlit as st
import tempfile
import os
import requests
try:
    import sounddevice as sd
except Exception:
    sd = None
import soundfile as sf
import numpy as np
from dotenv import load_dotenv
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from risk_engine import analyze_call

load_dotenv()
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

st.set_page_config(page_title="BhashaShield", page_icon="🛡️", layout="centered")

@st.cache_resource
def warmup():
    import numpy as np
    import tempfile
    import soundfile as sf
    dummy = np.zeros(16000, dtype=np.float32)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, dummy, 16000)
        tmp_path = f.name
    from deepfake_detector import deepfake_score
    deepfake_score(tmp_path)
    try:
        os.unlink(tmp_path)
    except Exception:
        pass
    return True

warmup()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background-color: #0f0f0f; }
.shield-header { text-align: center; padding: 2rem 0 1rem 0; }
.shield-title { font-size: 2.8rem; font-weight: 700; color: #ffffff; letter-spacing: -1px; }
.shield-sub { font-size: 1rem; color: #888; margin-top: 0.3rem; }
.risk-critical {
    background: linear-gradient(135deg, #3d0000, #1a0000);
    border: 1px solid #ff3333; border-radius: 16px;
    padding: 1.5rem 2rem; text-align: center;
}
.risk-high {
    background: linear-gradient(135deg, #2d1500, #1a0d00);
    border: 1px solid #ff8800; border-radius: 16px;
    padding: 1.5rem 2rem; text-align: center;
}
.risk-medium {
    background: linear-gradient(135deg, #1a1a00, #111100);
    border: 1px solid #cccc00; border-radius: 16px;
    padding: 1.5rem 2rem; text-align: center;
}
.risk-low {
    background: linear-gradient(135deg, #001a00, #001100);
    border: 1px solid #00cc44; border-radius: 16px;
    padding: 1.5rem 2rem; text-align: center;
}
.risk-score { font-size: 4rem; font-weight: 700; line-height: 1; }
.risk-label { font-size: 1.2rem; font-weight: 600; margin-top: 0.5rem;
              text-transform: uppercase; letter-spacing: 2px; }
.signal-box { background: #111; border: 1px solid #222; border-radius: 12px;
              padding: 1rem; text-align: center; }
.signal-val { font-size: 1.8rem; font-weight: 700; color: #fff; }
.signal-label { font-size: 0.75rem; color: #666; text-transform: uppercase;
                letter-spacing: 1px; margin-top: 0.2rem; }
.flag-chip-high {
    display: inline-block; background: #3d0000; border: 1px solid #ff4444;
    color: #ff8888; border-radius: 20px; padding: 4px 14px;
    font-size: 0.85rem; margin: 3px;
}
.flag-chip-medium {
    display: inline-block; background: #2d1500; border: 1px solid #ff8800;
    color: #ffaa44; border-radius: 20px; padding: 4px 14px;
    font-size: 0.85rem; margin: 3px;
}
.flag-chip-urgency {
    display: inline-block; background: #1a1500; border: 1px solid #ccaa00;
    color: #ddcc44; border-radius: 20px; padding: 4px 14px;
    font-size: 0.85rem; margin: 3px;
}
.transcript-box {
    background: #111; border: 1px solid #222; border-radius: 12px;
    padding: 1rem 1.2rem; color: #ccc; font-size: 0.95rem; line-height: 1.6;
}
.stButton>button {
    background: #fff; color: #000; border: none; border-radius: 10px;
    font-weight: 600; font-size: 1rem; padding: 0.6rem 2rem;
    width: 100%; transition: opacity 0.2s;
}
.stButton>button:hover { opacity: 0.85; }
</style>
""", unsafe_allow_html=True)


def transcribe_audio(wav_path):
    """Run STT twice — Hindi and English — combine both transcripts."""
    headers = {"api-subscription-key": SARVAM_API_KEY}

    # Hindi STT
    with open(wav_path, "rb") as f:
        r_hi = requests.post(
            "https://api.sarvam.ai/speech-to-text",
            headers=headers,
            files={"file": (wav_path, f, "audio/wav")},
            data={"language_code": "hi-IN", "model": "saarika:v2.5"}
        )
    transcript_devanagari = r_hi.json().get("transcript", "")

    # English STT
    with open(wav_path, "rb") as f:
        r_en = requests.post(
            "https://api.sarvam.ai/speech-to-text",
            headers=headers,
            files={"file": (wav_path, f, "audio/wav")},
            data={"language_code": "en-IN", "model": "saarika:v2.5"}
        )
    transcript_english = r_en.json().get("transcript", "")

    # Romanise the Hindi transcript
    transcript_roman = transliterate(
        transcript_devanagari, sanscript.DEVANAGARI, sanscript.ITRANS
    )

    # Combined transcript for keyword scoring — all three versions
    combined = f"{transcript_devanagari} {transcript_roman} {transcript_english}"

    return transcript_devanagari, transcript_english, combined


st.markdown("""
<div class="shield-header">
    <div class="shield-title">🛡️ BhashaShield</div>
    <div class="shield-sub">AI-powered fraud &amp; deepfake detection for Indian voice calls</div>
</div>
""", unsafe_allow_html=True)

st.divider()

if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

tab1, tab2 = st.tabs(["📂 Upload Recording", "🎙️ Record Live"])

with tab1:
    uploaded = st.file_uploader("Drop a .wav file here", type=["wav"],
                                label_visibility="collapsed")
    if uploaded:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded.read())
            st.session_state.audio_path = tmp.name
        st.audio(st.session_state.audio_path)

with tab2:
    st.markdown("#### Record up to 30 seconds")
    duration = st.slider("Duration (seconds)", 5, 30, 15)
    if st.button("⏺ Start Recording"):
        with st.spinner(f"Recording for {duration} seconds... speak now"):
            sample_rate = 16000
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate, channels=1, dtype='float32'
            )
            sd.wait()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            sf.write(tmp.name, recording, sample_rate)
            st.session_state.audio_path = tmp.name
        st.success("Recording complete!")
        st.audio(st.session_state.audio_path)

st.divider()

analyze = st.button("🔍 Analyze Call", type="primary", use_container_width=True)

if analyze:
    if not st.session_state.audio_path:
        st.error("Please upload or record audio first.")
    else:
        audio_path = st.session_state.audio_path

        with st.spinner("Step 1/2 — Transcribing (Hindi + English)..."):
            transcript_devanagari, transcript_english, combined = transcribe_audio(audio_path)

        if not transcript_devanagari and not transcript_english:
            st.error("Transcription failed — check your Sarvam API key in .env")
        else:
            with st.spinner("Step 2/2 — Analyzing audio signals (~3s)..."):
                result = analyze_call(audio_path, combined, transcript_devanagari)

            score = result["final_score"]

            if score >= 70:
                css_class, color, emoji = "risk-critical", "#ff4444", "🔴"
            elif score >= 55:
                css_class, color, emoji = "risk-high", "#ff8800", "🟠"
            elif score >= 30:
                css_class, color, emoji = "risk-medium", "#cccc00", "🟡"
            else:
                css_class, color, emoji = "risk-low", "#00cc44", "🟢"

            risk_label = result["risk_level"].split()[-1]

            st.markdown(f"""
            <div class="{css_class}">
                <div class="risk-score" style="color:{color}">{score}</div>
                <div class="risk-label" style="color:{color}">{emoji} {risk_label} Risk</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("**Signal Breakdown**")
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(f"""
                <div class="signal-box">
                    <div class="signal-val">{result['keyword_score']}</div>
                    <div class="signal-label">Keyword Score</div>
                </div>""", unsafe_allow_html=True)

            with c2:
                dp = result['deepfake_prob']
                dp_color = "#ff4444" if dp > 0.5 else "#00cc44"
                st.markdown(f"""
                <div class="signal-box">
                    <div class="signal-val" style="color:{dp_color}">{dp}</div>
                    <div class="signal-label">AI Voice Prob</div>
                </div>""", unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="signal-box">
                    <div class="signal-val">{result['language_switches']}</div>
                    <div class="signal-label">Lang Switches</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # show both transcripts
            st.markdown("**Transcript**")
            col_hi, col_en = st.columns(2)
            with col_hi:
                st.caption("Hindi (Devanagari)")
                st.markdown(
                    f'<div class="transcript-box">{transcript_devanagari or "—"}</div>',
                    unsafe_allow_html=True
                )
            with col_en:
                st.caption("English")
                st.markdown(
                    f'<div class="transcript-box">{transcript_english or "—"}</div>',
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)

            if result["keyword_flags"]:
                st.markdown("**Flagged Keywords**")
                chips = ""
                seen = set()
                for flag in result["keyword_flags"]:
                    w = flag["word"]
                    if w.lower() in seen:
                        continue
                    seen.add(w.lower())
                    tier = flag["tier"]
                    css = ("flag-chip-high" if tier == "high_risk"
                           else "flag-chip-medium" if tier == "medium_risk"
                           else "flag-chip-urgency")
                    chips += f'<span class="{css}">{w}</span>'
                st.markdown(chips, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

            if score >= 55:
                st.error(
                    "⚠️ **High fraud probability.** Do NOT share OTP, PIN, "
                    "Aadhaar, or any account details. Hang up and call your "
                    "bank on their official number."
                )
            elif score >= 30:
                st.warning(
                    "⚠️ **Suspicious elements detected.** "
                    "Be cautious and do not share sensitive information."
                )
            else:
                st.success("✅ **Call appears safe.** No major fraud indicators detected.")

            st.session_state.audio_path = None

st.divider()
st.markdown(
    "<center><small style='color:#444'>BhashaShield · "
    "Built for Indian voice fraud protection · IIIT Pune</small></center>",
    unsafe_allow_html=True
)
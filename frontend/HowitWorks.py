import streamlit as st
from utils import init_page

def app():
    init_page("How It Works")

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="title">📘 How SilentGuardian Works</div>
        <div class="subtitle">
            Step-by-step view of the AI pipeline.
        </div>

        <h4>1️⃣ Audio → Multilingual Speech Recognition</h4>
        <p>Whisper model converts speech (Hindi, English, Kannada, etc.) into text.</p>

        <h4>2️⃣ Transcript → Threat / Emotion Classification</h4>
        <p>Transformers model detects fear, anger, harassment & abusive terms.</p>

        <h4>3️⃣ Route & Sensors → Risk Engine</h4>
        <ul>
            <li>GPS Route Deviation</li>
            <li>Motion Struggle (accelerometer)</li>
            <li>Silent Trigger (hardware buttons)</li>
        </ul>

        <h4>4️⃣ Fusion → 0–100 Safety Score</h4>
        <p>Combines all signals to judge risk.</p>

        <h4>5️⃣ Evidence Storage</h4>
        <p>Transcript + audio bytes saved for legal protection.</p>

    </div>
    """, unsafe_allow_html=True)

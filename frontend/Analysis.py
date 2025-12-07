import streamlit as st
import requests
import pandas as pd
from utils import init_page

BACKEND_URL = "http://localhost:8000/analyze"

def app():
    init_page("Live Analysis")

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
        <div class="card">
            <div class="title">🔴 Live Threat Analysis</div>
            <div class="subtitle">
                Upload audio + simulated sensor values → SilentGuardian calculates risk score & SOS decision.
            </div>
        </div>
    """, unsafe_allow_html=True)

    audio = st.file_uploader("Upload Audio (wav/mp3/m4a)", type=["wav", "mp3", "m4a"])

    route_dev = st.slider("Route Deviation (meters)", 0, 500, 0)
    motion = st.slider("Motion Struggle (0–1)", 0.0, 1.0, 0.0)
    silent = st.checkbox("Silent Trigger Active?")

    if st.button("🚀 Run Analysis"):
        if audio is None:
            st.error("Upload audio first.")
            return

        with st.spinner("Analyzing..."):
            files = {"audio": (audio.name, audio.read(), audio.type)}
            data = {
                "route_deviation_meters": str(route_dev),
                "motion_struggle_score": str(motion),
                "silent_trigger": str(silent).lower(),
            }

            resp = requests.post(BACKEND_URL, files=files, data=data)

            if resp.status_code != 200:
                st.error(f"Error: {resp.text}")
                return

            out = resp.json()

            # Display risk score
            score = out["risk_score"]
            if score >= 70:
                color = "red"
            elif score >= 40:
                color = "orange"
            else:
                color = "green"

            st.markdown(
                f"""
                <div class="card">
                    <h2 style="color:{color}; text-align:center;">Risk Score: {score:.1f}</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if out["sos_triggered"]:
                st.error("🚨 SOS Recommended")
            else:
                st.success("No SOS Required")

            st.markdown("### 🗣 Transcript")
            st.code(out["transcript"])

            st.markdown("### 🔍 Audio Classification")
            st.json(out["audio_classification"])

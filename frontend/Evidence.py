import streamlit as st
import os
import json
from utils import init_page

def app():
    init_page("Evidence")

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
        <div class="card">
            <div class="title">📂 Incident Evidence</div>
            <div class="subtitle">
                SilentGuardian stores transcripts, audio and risk snapshots for unsafe events.
            </div>
        </div>
    """, unsafe_allow_html=True)

    evidence_folder = "evidence/"  # adjust if needed

    if not os.path.exists(evidence_folder):
        st.warning("No evidence collected yet.")
        return

    items = os.listdir(evidence_folder)

    for file in items:
        if file.endswith(".json"):
            with open(os.path.join(evidence_folder, file), "r") as f:
                data = json.load(f)

            st.markdown(f"""
            <div class="card">
                <h3 style="color:#38bdf8;">📝 Incident: {file}</h3>
                <p><strong>Risk Score:</strong> {data['risk_score']}</p>
                <p><strong>Transcript:</strong> {data['transcript']}</p>
            </div>
            """, unsafe_allow_html=True)

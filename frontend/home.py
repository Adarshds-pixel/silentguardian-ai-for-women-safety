import streamlit as st
from utils import init_page

def app():
    init_page("Home")

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
        <div class="card">
            <div class="title">🛡️ SilentGuardian AI</div>
            <div class="subtitle">
                Advanced multimodal women's-safety system powered by speech analysis, 
                motion detection, GPS route deviation & silent triggers.
            </div>

            <h4 style="color:#38bdf8;">Why this is different?</h4>
            <ul style="color:#cbd5e1; font-size:0.92rem; line-height:1.6;">
                <li>Understands real-time audio (multilingual)</li>
                <li>Detects distress, fear, harassment & abusive tone</li>
                <li>Tracks safe-route deviation during Safe Walk mode</li>
                <li>Detects violent motion struggle</li>
                <li>Silent button-trigger for hidden SOS</li>
                <li>Stores transcripts + audio as evidence</li>
            </ul>

            <hr style="border-color:#334155; margin-top:20px;">

            <p style="color:#94a3b8; font-size:0.85rem;">
            Use the navigation bar above to explore demos and features.
            </p>
        </div>
    """, unsafe_allow_html=True)

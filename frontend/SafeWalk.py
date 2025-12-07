import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils import init_page

def app():
    init_page("Safe Walk")

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="title">🧭 Safe Walk Mode</div>
        <div class="subtitle">
            User selects start & destination. SilentGuardian monitors if the user deviates 
            from expected walking route.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🏁 Select Start & Destination")

    places = ["Home", "Hostel", "College", "Office", "Bus Stop", "Metro Station"]

    start = st.selectbox("Start Location", places, index=1)
    dest = st.selectbox("Destination", places, index=2)

    eta_default = (datetime.now() + timedelta(minutes=25)).time()
    eta = st.time_input("Expected Arrival Time", value=eta_default)

    st.caption("This ETA is only for UI display; backend does not use it.")

    st.markdown("---")

    st.markdown("### 📍 Route Map (Simulated)")

    coords = {
        "Home": (12.9716, 77.5946),
        "Hostel": (12.9352, 77.6245),
        "College": (12.9850, 77.6050),
        "Office": (12.9755, 77.6050),
        "Bus Stop": (12.9660, 77.6000),
        "Metro Station": (12.9701, 77.5930),
    }

    lat1, lon1 = coords[start]
    lat2, lon2 = coords[dest]

    df = pd.DataFrame(
        [
            {"lat": lat1, "lon": lon1},
            {"lat": lat2, "lon": lon2},
        ]
    )

    st.map(df)

    st.info("Safe Walk mode ready. Actual deviation detection happens in Analysis page.")

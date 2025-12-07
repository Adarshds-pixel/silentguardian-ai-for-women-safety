# frontend/streamlit_app.py

import requests
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

BACKEND_URL = "http://localhost:8000/analyze"  # FastAPI backend

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="SilentGuardian AI – Threat Detection Engine",
    page_icon="🛡",
    layout="wide",
)

# ---------- CYBER NEON CSS ----------
st.markdown(
    """
    <style>
    @keyframes cyberGradient {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }
    @keyframes scanLines {
        0% { background-position: 0 0; }
        100% { background-position: 0 8px; }
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(59, 130, 246, 0.25) 0, transparent 40%),
            radial-gradient(circle at top right, rgba(14, 116, 144, 0.35) 0, transparent 45%),
            radial-gradient(circle at bottom, rgba(15, 23, 42, 0.95) 0, #020617 60%);
        background-size: 200% 200%;
        animation: cyberGradient 32s ease infinite;
        color: #e5e7eb;
        font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image: linear-gradient(
            rgba(15,23,42,0.18) 1px,
            transparent 2px
        );
        background-size: 100% 3px;
        opacity: 0.28;
        mix-blend-mode: soft-light;
        animation: scanLines 12s linear infinite;
        z-index: -1;
    }
    .stApp::after {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image:
            linear-gradient(rgba(30, 64, 175, 0.25) 1px, transparent 1px),
            linear-gradient(90deg, rgba(30, 64, 175, 0.25) 1px, transparent 1px);
        background-size: 70px 70px;
        opacity: 0.12;
        z-index: -1;
    }

    .main-card {
        background: rgba(15, 23, 42, 0.94);
        border-radius: 20px;
        padding: 18px 22px 20px 22px;
        border: 1px solid rgba(56, 189, 248, 0.45);
        box-shadow:
            0 18px 40px rgba(15, 23, 42, 0.95),
            0 0 0 1px rgba(15, 23, 42, 1);
        backdrop-filter: blur(18px);
        position: relative;
        overflow: hidden;
        transition: transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s ease;
    }
    .main-card::before {
        content: "";
        position: absolute;
        inset: -2px;
        background: conic-gradient(
            from 180deg,
            rgba(56,189,248,0.0),
            rgba(56,189,248,0.65),
            rgba(129,140,248,0.6),
            rgba(56,189,248,0.0)
        );
        opacity: 0;
        transition: opacity 0.32s ease;
        filter: blur(12px);
        z-index: -1;
    }
    .main-card:hover::before { opacity: 0.9; }
    .main-card:hover {
        transform: translateY(-3px);
        box-shadow:
            0 26px 55px rgba(15, 23, 42, 1),
            0 0 0 1px rgba(56, 189, 248, 0.8);
        border-color: rgba(125, 211, 252, 0.9);
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.15rem;
        color: #e5e7eb;
        letter-spacing: 0.02em;
    }
    .section-caption {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-bottom: 0.7rem;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 11px;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 500;
        border: 1px solid rgba(148, 163, 184, 0.7);
        margin-right: 6px;
        margin-bottom: 4px;
        gap: 6px;
        transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease, background 0.16s ease;
        cursor: default;
    }
    .badge:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 22px rgba(15, 23, 42, 0.9);
        border-color: rgba(248, 250, 252, 0.9);
        background: rgba(15, 23, 42, 0.95);
    }
    .badge-dot {
        width: 7px;
        height: 7px;
        border-radius: 999px;
    }
    .badge-danger-high { background: rgba(239, 68, 68, 0.12); border-color: rgba(248, 113, 113, 0.9); }
    .badge-danger-medium { background: rgba(245, 158, 11, 0.12); border-color: rgba(252, 211, 77, 0.9); }
    .badge-danger-low { background: rgba(34, 197, 94, 0.1); border-color: rgba(74, 222, 128, 0.9); }
    .badge-danger-none { background: rgba(34, 197, 94, 0.08); border-color: rgba(34, 197, 94, 0.8); }

    .badge-emotion { background: rgba(59, 130, 246, 0.14); border-color: rgba(96, 165, 250, 0.95); }
    .badge-abuse-yes { background: rgba(239, 68, 68, 0.14); border-color: rgba(252, 165, 165, 0.95); }
    .badge-abuse-no { background: rgba(22, 163, 74, 0.18); border-color: rgba(187, 247, 208, 0.95); }

    .risk-circle {
        width: 146px;
        height: 146px;
        border-radius: 50%;
        border: 13px solid transparent;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 0.6rem auto;
        position: relative;
        box-sizing: border-box;
    }
    .risk-circle-inner {
        width: 96px;
        height: 96px;
        border-radius: 999px;
        background:
            radial-gradient(circle at top, #1d4ed8 0, #020617 60%),
            radial-gradient(circle at bottom, #020617 0, #020617 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        box-shadow: inset 0 0 14px rgba(15, 23, 42, 0.9);
    }
    .risk-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #cbd5f5;
    }
    .risk-score {
        font-size: 1.6rem;
        font-weight: 750;
    }
    .risk-low { border-color: rgba(34, 197, 94, 0.95); box-shadow: 0 0 30px rgba(34, 197, 94, 0.55); }
    .risk-medium { border-color: rgba(245, 158, 11, 0.98); box-shadow: 0 0 32px rgba(245, 158, 11, 0.7); }
    .risk-high { border-color: rgba(239, 68, 68, 1); box-shadow: 0 0 36px rgba(239, 68, 68, 0.95); }

    @keyframes sosPulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(248, 113, 113, 0.7); }
        60% { transform: scale(1.025); box-shadow: 0 0 36px 18px rgba(248, 113, 113, 0.0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(248, 113, 113, 0.0); }
    }
    .sos-card {
        border-radius: 14px;
        border: 1px solid rgba(248, 113, 113, 0.9);
        background: radial-gradient(circle at top, rgba(148, 27, 37, 0.96) 0, rgba(15, 23, 42, 0.98) 60%);
        padding: 10px 14px;
        display: flex;
        gap: 10px;
        align-items: flex-start;
        animation: sosPulse 1.6s infinite;
    }
    .sos-icon { font-size: 1.6rem; margin-top: 2px; }

    .transcript-box {
        background: rgba(15, 23, 42, 0.96);
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.72);
        padding: 10px 12px;
        font-size: 0.9rem;
        max-height: 230px;
        overflow-y: auto;
        box-shadow: inset 0 0 18px rgba(15, 23, 42, 0.95);
    }

    .top-header-title {
        font-size: 1.88rem;
        font-weight: 780;
        letter-spacing: 0.06em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .top-header-subtitle {
        font-size: 0.9rem;
        color: #9ca3af;
        max-width: 640px;
    }

    .shield-icon {
        width: 30px;
        height: 30px;
        border-radius: 10px;
        background: radial-gradient(circle at top, #38bdf8 0, #1d4ed8 50%, #020617 100%);
        box-shadow: 0 0 18px rgba(56, 189, 248, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }

    .pill-online {
        font-size: 0.75rem;
        padding: 3px 10px;
        border-radius: 999px;
        border: 1px solid rgba(56, 189, 248, 0.92);
        background: radial-gradient(circle at top, rgba(56,189,248,0.35) 0, rgba(15,23,42,0.96) 70%);
        color: #e0f2fe;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    .pill-dot {
        width: 7px;
        height: 7px;
        border-radius: 999px;
        background: #22c55e;
        box-shadow: 0 0 12px rgba(34, 197, 94, 0.9);
    }

    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        padding: 6px 12px;
        border-radius: 999px;
        background-color: rgba(15, 23, 42, 0.96);
        border: 1px solid rgba(37, 99, 235, 0.9);
        color: #e5e7eb;
    }
    .stTabs [data-baseweb="tab"]:hover {
        border-color: rgba(125, 211, 252, 0.98);
        background-color: rgba(15, 23, 42, 0.98);
    }

    div.stButton > button {
        width: 100%;
        border-radius: 999px;
        border: 1px solid rgba(59, 130, 246, 0.92);
        background: linear-gradient(135deg, #1d4ed8 0%, #0ea5e9 50%, #020617 100%);
        color: #e5e7eb;
        font-weight: 600;
        padding-top: 0.55rem;
        padding-bottom: 0.55rem;
        transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease, filter 0.16s ease;
        background-size: 180% 180%;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 34px rgba(37, 99, 235, 0.9);
        border-color: rgba(191, 219, 254, 1);
        filter: brightness(1.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HEADER ----------
col_header_left, col_header_right = st.columns([3, 1])

with col_header_left:
    st.markdown(
        """
        <div>
            <div class="top-header-title">
                <div class="shield-icon">🛡</div>
                <div>SilentGuardian <span style="opacity:0.70;">AI</span></div>
            </div>
            <div class="top-header-subtitle">
                Cyber-grade multimodal threat analysis engine for women's safety – 
                combining audio understanding with simulated route deviation, motion struggle, 
                and silent triggers into a single risk score.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_header_right:
    st.markdown(
        """
        <div style="display:flex;justify-content:flex-end;margin-top:8px;">
            <div class="pill-online">
                <span class="pill-dot"></span>
                Core AI Engine Online
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption(
    "Supports multilingual audio – English, Hindi, Kannada, Telugu, Tamil and more, "
    "auto-detected by the speech model running in the backend."
)

st.markdown("")  # spacing

# ---------- TABS ----------
tab_live, tab_how = st.tabs(["🔴 Live Analysis", "📘 How it works"])

# ---------- TAB 1: LIVE ANALYSIS ----------
with tab_live:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    left_col, right_col = st.columns([1.05, 1.1])

    # ---- LEFT: INPUT ----
    with left_col:
        st.markdown('<div class="section-title">1. Input Signal</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">Upload ambient audio and configure simulated phone sensor readings.</div>',
            unsafe_allow_html=True,
        )

        # 🧭 SAFE WALK MODE UI (Method A)
        st.markdown("#### 🧭 Safe Walk Mode (demo)")
        st.caption(
            "User starts a safe walk by selecting start and destination. "
            "SilentGuardian monitors deviation from this expected route."
        )

        safe_walk_enabled = st.checkbox(
            "Enable Safe Walk monitoring", value=True,
            help="When enabled, route deviation is interpreted as moving away from this safe path."
        )

        places = ["Home", "Hostel / PG", "College", "Office"]
        start_place = st.selectbox("Start from", places, index=1)
        destination = st.selectbox("Destination", places, index=2)

        # Optional ETA just for UI (not used in backend)
        #eta = st.time_input("Expected arrival time (optional)", value=eta_default)

        eta_default = (datetime.now() + timedelta(minutes=30)).time()
        eta = st.time_input(
            "Expected arrival time (optional)",
            value=eta_default,
            key="eta_input"
        )


        st.markdown("---")

        audio_file = st.file_uploader(
            "Upload environment audio (wav/mp3/m4a)",
            type=["wav", "mp3", "m4a"],
            label_visibility="collapsed",
        )

        st.markdown("<br/>", unsafe_allow_html=True)

        st.markdown('<div class="section-title">2. Sensor Fusion (Simulated)</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">In the full mobile app, these values stream live from GPS, accelerometer, and button patterns.</div>',
            unsafe_allow_html=True,
        )

        route_deviation = st.slider(
            "Route deviation from safe path (meters)",
            min_value=0,
            max_value=500,
            value=0,
            step=10,
            help="How far the user is from their expected safe route.",
        )

        motion_struggle = st.slider(
            "Motion struggle score (0 = calm, 1 = violent struggle)",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            help="Simulated intensity of abnormal/shaky movement of the phone.",
        )

        silent_trigger = st.checkbox(
            "Silent distress trigger activated (e.g., volume button pattern)",
            value=False,
            help="Simulates the user secretly pressing a distress pattern on hardware buttons.",
        )

        # Quick scenario presets for demo
        preset = st.radio(
            "Quick scenario presets",
            ["None", "👩‍🎓 Safe walk home", "⚠ Suspicious situation", "🚨 High-risk incident"],
            index=0,
        )

        # Effective values (what we actually send to backend)
        eff_route = route_deviation
        eff_motion = motion_struggle
        eff_silent = silent_trigger

        if preset == "👩‍🎓 Safe walk home":
            eff_route = 0
            eff_motion = 0.0
            eff_silent = False
        elif preset == "⚠ Suspicious situation":
            eff_route = 150
            eff_motion = 0.4
            eff_silent = False
        elif preset == "🚨 High-risk incident":
            eff_route = 350
            eff_motion = 0.9
            eff_silent = True

        st.caption(
            f"Effective values → Route deviation: {eff_route} m, "
            f"Motion struggle: {eff_motion:.1f}, Silent trigger: {eff_silent}"
        )

        # ---------- GPS ROUTE VISUAL (SIMULATED SAFE WALK) ----------
        st.markdown("#### 📍 Route visual (simulated)")
        st.caption(
            f"Monitoring safe walk: {start_place} ➝ {destination}. "
            "Blue pin = expected route, red pin = current location shifted by route deviation."
        )

        # Simple fake coordinates for locations around Bengaluru
        location_coords = {
            "Home": (12.9716, 77.5946),
            "Hostel / PG": (12.9352, 77.6245),
            "College": (12.9850, 77.6050),
            "Office": (12.9755, 77.6050),
        }

        start_lat, start_lon = location_coords[start_place]
        dest_lat, dest_lon = location_coords[destination]

        # Convert meters to degrees (very rough approximation)
        deviation_deg = eff_route / 111_000.0  # 1 degree ~ 111 km

        # Current location is simulated as deviating north from the expected route near destination
        current_lat = dest_lat + deviation_deg
        current_lon = dest_lon

        df_points = pd.DataFrame(
            [
                {"lat": start_lat, "lon": start_lon},      # Start
                {"lat": dest_lat, "lon": dest_lon},        # Destination (expected)
                {"lat": current_lat, "lon": current_lon},  # Current (possibly deviated)
            ]
        )

        st.map(df_points)

        st.markdown("<br/>", unsafe_allow_html=True)

        analyze_btn = st.button("🚀 Run SilentGuardian Analysis")

    # ---- RIGHT: OUTPUT ----
    with right_col:
        st.markdown('<div class="section-title">3. AI Safety Intelligence</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">Transcript understanding, emotion, and fused risk score from the SilentGuardian AI engine.</div>',
            unsafe_allow_html=True,
        )

        if analyze_btn:
            if audio_file is None:
                st.error("Please upload an audio file to analyze.")
            else:
                with st.spinner("Analyzing environment using SilentGuardian AI..."):
                    files = {
                        "audio": (audio_file.name, audio_file.read(), audio_file.type or "application/octet-stream")
                    }
                    data = {
                        "route_deviation_meters": str(eff_route),
                        "motion_struggle_score": str(eff_motion),
                        "silent_trigger": "true" if eff_silent else "false",
                    }

                    try:
                        resp = requests.post(BACKEND_URL, files=files, data=data, timeout=180)
                    except Exception as e:
                        st.error(f"Could not contact backend. Is the FastAPI server running?\n\nDetails: {e}")
                    else:
                        if resp.status_code != 200:
                            st.error(
                                f"Backend error (status {resp.status_code}).\n\n"
                                f"Response:\n{resp.text}"
                            )
                        else:
                            result = resp.json()
                            transcript = result.get("transcript", "")
                            audio_class = result.get("audio_classification", {})
                            risk_score = result.get("risk_score", 0.0)
                            sos_triggered = result.get("sos_triggered", False)

                            if risk_score >= 70:
                                risk_class = "risk-high"
                                risk_label = "High Risk"
                            elif risk_score >= 40:
                                risk_class = "risk-medium"
                                risk_label = "Medium Risk"
                            else:
                                risk_class = "risk-low"
                                risk_label = "Low Risk"

                            st.markdown("<br/>", unsafe_allow_html=True)

                            st.markdown(
                                f"""
                                <div style="display:flex;flex-direction:column;align-items:center;margin-bottom:1.0rem;">
                                    <div class="risk-circle {risk_class}">
                                        <div class="risk-circle-inner">
                                            <div class="risk-label">{risk_label}</div>
                                            <div class="risk-score">{risk_score:.1f}</div>
                                        </div>
                                    </div>
                                    <div style="font-size:0.84rem;color:#9ca3af;">
                                        Fused risk from audio, emotion, route deviation, motion struggle, and silent trigger.
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                            if sos_triggered:
                                st.markdown(
                                    """
                                    <div class="sos-card">
                                        <div class="sos-icon">🚨</div>
                                        <div>
                                            <div style="font-weight:600;margin-bottom:4px;">SOS Recommended</div>
                                            <div style="font-size:0.86rem;color:#fee2e2;">
                                                SilentGuardian would trigger an emergency alert in this scenario – high-risk multi-signal pattern detected.
                                            </div>
                                        </div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                            else:
                                st.success(
                                    "✅ No SOS: Risk below threshold. SilentGuardian continues passive background monitoring."
                                )

                            st.markdown("---")

                            danger_level = audio_class.get("danger_level", "unknown")
                            abusive = audio_class.get("has_abusive_keywords", False)
                            emotion = audio_class.get("emotion", "unknown")
                            reason = audio_class.get("reason", "")

                            if danger_level == "high":
                                dl_class = "badge-danger-high"
                            elif danger_level == "medium":
                                dl_class = "badge-danger-medium"
                            elif danger_level == "low":
                                dl_class = "badge-danger-low"
                            else:
                                dl_class = "badge-danger-none"

                            st.markdown(
                                f"""
                                <div style="margin-bottom:0.5rem;">
                                    <span class="badge {dl_class}">
                                        <span class="badge-dot" style="background:#f97373;"></span>
                                        Danger: {danger_level.capitalize()}
                                    </span>
                                    <span class="badge badge-emotion">
                                        <span class="badge-dot" style="background:#60a5fa;"></span>
                                        Emotion: {emotion.capitalize()}
                                    </span>
                                    <span class="badge {'badge-abuse-yes' if abusive else 'badge-abuse-no'}">
                                        <span class="badge-dot" style="background:{'#ef4444' if abusive else '#22c55e'};"></span>
                                        Abusive Language: {"Yes" if abusive else "No"}
                                    </span>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                            if reason:
                                st.caption(f"AI reasoning: {reason}")

                            st.markdown("#### 🗣 Transcript")
                            if transcript.strip():
                                st.markdown(
                                    f'<div class="transcript-box">{transcript}</div>',
                                    unsafe_allow_html=True,
                                )
                            else:
                                st.info("No transcript returned. Try a clearer or slightly longer audio sample.")

                            st.markdown("")
                            st.caption(
                                "Note: This demo uses sliders and presets to simulate phone sensors. "
                                "In the full mobile app, values will stream automatically from GPS, accelerometer, and hardware buttons."
                            )
        else:
            st.info("Upload an audio clip on the left, choose a scenario preset, and click *Run SilentGuardian Analysis*.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- TAB 2: HOW IT WORKS ----------
with tab_how:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### 📘 How SilentGuardian AI Works")

    st.markdown(
        """
1. *Ambient Audio Capture*  
   In the full system, a mobile app continuously captures short audio snippets when protection mode is ON.

2. *Multilingual Speech Understanding (Local AI Backend)*  
   The backend runs an open-source Whisper model (via faster-whisper) to convert speech to text in many 
   languages (English, Hindi, Kannada, Telugu, Tamil, etc.).  
   A local Transformers model then:
   - Estimates sentiment / emotional tone  
   - Detects harassment or threats  
   - Flags abusive or threat-like language

3. *Safe Walk Mode & Sensor Fusion for Risk Scoring*  
   The user starts a Safe Walk by selecting *start* and *destination*.  
   The system knows the expected route and fuses:
   - *Route deviation* – distance from the safe path  
   - *Motion struggle* – abnormal shaking or struggle from accelerometer  
   - *Silent triggers* – secret hardware button patterns  
   - *Audio distress* – threatening / abusive speech  

   These signals are combined into a *0–100 risk score* via a custom risk engine.

4. *SOS Decision & Evidence Capture*  
   If the risk score crosses a threshold (for example, 60+), SilentGuardian will:
   - Recommend SOS (as in this demo), and  
   - In the full backend, save audio + transcript + sensor snapshot as evidence for the incident.

5. *Why this is different from normal SOS apps*  
   - Goes beyond a simple one-tap SOS  
   - Uses *multimodal AI* (audio + motion + route + triggers)  
   - Works even if the victim cannot speak openly or unlock the phone  
   - Uses *privacy-friendly local models*, so analysis can run without constant cloud access.
        """
    )

    st.markdown("</div>", unsafe_allow_html=True)
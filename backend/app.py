# backend/app.py

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pathlib import Path
from datetime import datetime
import json

from backend.audio_processor import transcribe_audio
from backend.gpt_classifier import classify_transcript
from backend.risk_engine import compute_risk_score, is_sos_required
from backend.models import AnalysisResult


app = FastAPI(
    title="SilentGuardian AI Backend (Free Models)",
    description=(
        "Core risk engine for SilentGuardian – uses local Whisper and Transformers "
        "models to analyze audio and simulated sensor readings, estimate danger level, "
        "and decide whether to trigger SOS. No paid APIs are required."
    ),
    version="0.2.0",
)

# CORS so frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging last events (optional)
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
EVENT_FILE = LOG_DIR / "events.json"

EVIDENCE_DIR = LOG_DIR / "evidence"
EVIDENCE_DIR.mkdir(exist_ok=True)


def append_event(event: dict) -> None:
    """Store last ~20 events in logs/events.json (best-effort, non-fatal)."""
    try:
        if EVENT_FILE.exists():
            data = json.loads(EVENT_FILE.read_text(encoding="utf-8"))
        else:
            data = []
        if not isinstance(data, list):
            data = []
        data.append(event)
        data = data[-20:]
        EVENT_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


def save_evidence(
    evidence_id: str,
    audio_bytes: bytes,
    transcript: str,
    audio_classification: dict,
    sensors: dict,
    risk_score: float,
    sos_triggered: bool,
) -> None:
    """
    Save evidence for high-risk events:
    - WAV audio file
    - JSON metadata
    """
    try:
        # 1) Audio
        audio_path = EVIDENCE_DIR / f"{evidence_id}_audio.wav"
        with open(audio_path, "wb") as f:
            f.write(audio_bytes)

        # 2) Metadata
        meta = {
            "evidence_id": evidence_id,
            "transcript": transcript,
            "audio_classification": audio_classification,
            "sensors": sensors,
            "risk_score": risk_score,
            "sos_triggered": sos_triggered,
            "saved_at": datetime.utcnow().isoformat() + "Z",
        }
        meta_path = EVIDENCE_DIR / f"{evidence_id}_meta.json"
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        # Evidence saving must never break the main API
        pass


@app.get("/", response_class=HTMLResponse, tags=["System"])
def root():
    return """
    <html>
        <body style="font-family:Segoe UI, Arial; background:#020617; color:#e5e7eb; padding:40px;">
            <h1 style="color:#38bdf8;">🛡️ SilentGuardian AI Backend (Free Models)</h1>
            <p>Core risk engine is running successfully using only local open-source models.</p>
            <p style="margin-top:10px; color:#9ca3af;">
                Use this backend with the SilentGuardian Streamlit frontend or a future mobile app.
            </p>
            <p style="margin-top:20px;">
                👉 <a href="/docs" style="color:#93c5fd; font-size:18px; text-decoration:none;">
                    Open API Documentation (Swagger UI)
                </a>
            </p>
        </body>
    </html>
    """


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "service": "SilentGuardian AI Backend (Free Models)",
        "version": "0.2.0",
    }


@app.post(
    "/analyze",
    response_model=AnalysisResult,
    summary="Analyze audio + sensor data for threat level",
    description=(
        "Upload an environment audio clip along with simulated phone sensor values. "
        "The backend transcribes the audio (multilingual) using a local Whisper model, "
        "classifies sentiment and abusive language with a Transformers model, "
        "computes a 0–100 risk score, and decides if SOS should be triggered."
    ),
)
async def analyze(
    audio: UploadFile = File(...),
    route_deviation_meters: float = Form(...),
    motion_struggle_score: float = Form(...),
    silent_trigger: bool = Form(...),
):
    # 1) Transcription + local classification
    try:
        audio_bytes = await audio.read()
        transcript = transcribe_audio(audio_bytes, filename=audio.filename)
        audio_classification = classify_transcript(transcript)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=(
                "Local AI models failed while processing audio. "
                "Check console logs or model installation."
            ),
        ) from e

    # 2) Risk fusion
    risk_score = compute_risk_score(
        audio_danger_level=audio_classification.get("danger_level", "none"),
        has_abusive_keywords=audio_classification.get("has_abusive_keywords", False),
        emotion=audio_classification.get("emotion", "neutral"),
        route_deviation_meters=route_deviation_meters,
        motion_struggle_score=motion_struggle_score,
        silent_trigger=silent_trigger,
    )

       # 3) SOS decision
    sos = is_sos_required(risk_score)

    # 4) Log event
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "risk_score": risk_score,
        "sos_triggered": sos,
        "danger_level": audio_classification.get("danger_level", "none"),
        "silent_trigger": silent_trigger,
        "route_deviation_meters": route_deviation_meters,
        "motion_struggle_score": motion_struggle_score,
    }
    append_event(event)

    # 5) Save evidence only for SOS cases
    if sos:
        safe_id = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        sensors = {
            "route_deviation_meters": route_deviation_meters,
            "motion_struggle_score": motion_struggle_score,
            "silent_trigger": silent_trigger,
        }
        save_evidence(
            evidence_id=safe_id,
            audio_bytes=audio_bytes,
            transcript=transcript,
            audio_classification=audio_classification,
            sensors=sensors,
            risk_score=risk_score,
            sos_triggered=sos,
        )

    # 6) Structured response
    return AnalysisResult(
        transcript=transcript,
        audio_classification=audio_classification,
        risk_score=risk_score,
        sos_triggered=sos,
    )

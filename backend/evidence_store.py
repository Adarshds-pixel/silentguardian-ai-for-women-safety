import json
import uuid
from datetime import datetime
from pathlib import Path
from settings import settings # type: ignore

def save_incident(
    transcript: str,
    audio_bytes: bytes,
    audio_filename: str,
    risk_score: float,
    reasons: list,
    audio_classification: dict,
    route_deviation_meters: float,
    motion_struggle_score: float,
    silent_trigger: bool,
):

    base = settings.evidence_base_dir
    base.mkdir(exist_ok=True)

    incident_id = datetime.utcnow().strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:6]
    folder = base / incident_id
    folder.mkdir()

    audio_path = folder / audio_filename
    audio_path.write_bytes(audio_bytes)

    meta = {
        "incident_id": incident_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "transcript": transcript,
        "risk_score": risk_score,
        "reasons": reasons,
        "audio_classification": audio_classification,
        "sensors": {
            "route_deviation_meters": route_deviation_meters,
            "motion_struggle_score": motion_struggle_score,
            "silent_trigger": silent_trigger,
        }
    }

    (folder / "meta.json").write_text(json.dumps(meta, indent=2))
    return {"incident_id": incident_id}

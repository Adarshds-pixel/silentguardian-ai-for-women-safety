# backend/risk_engine.py

"""
Risk engine: combines audio classification + sensor values into a 0–100 risk score.
No external APIs, purely custom logic.
"""

from typing import Literal

DangerLevel = Literal["none", "low", "medium", "high"]
Emotion = Literal["calm", "fear", "anger", "panic", "neutral"]


def compute_risk_score(
    audio_danger_level: DangerLevel,
    has_abusive_keywords: bool,
    emotion: Emotion,
    route_deviation_meters: float,
    motion_struggle_score: float,
    silent_trigger: bool,
) -> float:
    """
    Fuses different signals into a single risk score (0–100).
    """

    score = 0.0

    # 1) Base score from audio danger level
    if audio_danger_level == "high":
        score += 50
    elif audio_danger_level == "medium":
        score += 30
    elif audio_danger_level == "low":
        score += 10
    else:
        score += 0

    # 2) Abusive keywords boost
    if has_abusive_keywords:
        score += 15

    # 3) Emotion boost
    if emotion in ["fear", "panic"]:
        score += 15
    elif emotion == "anger":
        score += 10
    elif emotion == "calm":
        score -= 5  # slight reduction
    # neutral -> no change

    # 4) Route deviation (0–500 m -> up to +15)
    route_factor = min(max(route_deviation_meters, 0), 500) / 500.0
    score += route_factor * 15.0

    # 5) Motion struggle (0–1 -> up to +15)
    motion_factor = min(max(motion_struggle_score, 0.0), 1.0)
    score += motion_factor * 15.0

    # 6) Silent trigger strongly increases risk
    if silent_trigger:
        score += 20

    # Normalize & clamp 0–100
    score = max(0.0, min(100.0, score))
    return round(score, 1)


def is_sos_required(risk_score: float, threshold: float = 60.0) -> bool:
    """
    Returns True if risk score is above SOS threshold.
    """
    return risk_score >= threshold

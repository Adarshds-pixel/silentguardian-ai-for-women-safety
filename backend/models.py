# backend/models.py

from pydantic import BaseModel, Field
from typing import Dict, Any


class AnalysisResult(BaseModel):
    """
    Standardized response model for the /analyze endpoint.
    """

    transcript: str = Field(
        ...,
        description="Text transcription of the uploaded audio (multilingual).",
        example="Help me! Leave me alone!",
    )

    audio_classification: Dict[str, Any] = Field(
        ...,
        description=(
            "Safety classification containing: danger_level, emotion, "
            "has_abusive_keywords, and a short reasoning string."
        ),
        example={
            "danger_level": "high",
            "emotion": "fear",
            "has_abusive_keywords": True,
            "reason": "Detected shouting, crying tone, and threatening statements."
        },
    )

    risk_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Overall fused risk score between 0 and 100.",
        example=82.5,
    )

    sos_triggered: bool = Field(
        ...,
        description="True if risk_score is above the SOS threshold.",
        example=True,
    )

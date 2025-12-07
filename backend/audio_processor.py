# backend/audio_processor.py

"""
Audio transcription using free, local Whisper model (via faster-whisper).

- No API key required
- Supports many languages (English, Hindi, Kannada, Telugu, Tamil, etc.)
- Runs fully on your machine
"""

from faster_whisper import WhisperModel
import tempfile
from pathlib import Path

# Choose model size:
# "tiny", "base", "small", "medium", "large-v2"
# tiny/base are fastest; medium/large are more accurate but heavier.
MODEL_SIZE = "small"

# Load once at startup so it is reused for every request.
# device="cpu" -> works on any machine; if you have GPU, you can try "cuda".
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")


def transcribe_audio(audio_bytes: bytes, filename: str = "audio.wav") -> str:
    """
    Transcribes audio bytes into text using the local Whisper model.
    Returns the full transcript as a string.

    This function:
    1. Writes bytes to a temporary file.
    2. Runs the Whisper model.
    3. Joins all segments into a single text string.
    """

    # 1) Save to a temporary file on disk
    suffix = Path(filename).suffix or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(audio_bytes)
        temp_path = temp.name

    # 2) Run transcription
    segments, info = model.transcribe(temp_path)

    # 3) Build the final text
    transcript_parts = [seg.text.strip() for seg in segments if seg.text]
    transcript = " ".join(transcript_parts).strip()

    if not transcript:
        transcript = "[No speech detected or audio too noisy]"

    return transcript

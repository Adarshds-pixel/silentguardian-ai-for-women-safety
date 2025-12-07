# backend/gpt_classifier.py

"""
Free text-based safety classifier using HuggingFace Transformers.

- Uses a multilingual sentiment model to estimate how negative the situation is.
- Uses multilingual abusive / threat keyword lists (English + Indian languages).
- Outputs:
    - danger_level: none | low | medium | high
    - emotion: calm | fear | anger | panic | neutral
    - has_abusive_keywords: bool
    - reason: short explanation
"""

from transformers import pipeline

# Multilingual sentiment model: labels like "1 star" ... "5 stars"
sentiment_model = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

# ---- MULTILINGUAL ABUSIVE/THREAT KEYWORDS ----
MULTILINGUAL_DANGER_PHRASES = {
    "kannada": [
        # Distress
        "sahaya madi", "nannage sahaya beku", "dayavittu rakshisi", "nanna ulisi",
        "nanna kapadi", "nannage help madi", "nange apaya ide", "nannage baya agutte",
        "bidi nanna", "kai bidu", "kai haakbeda",

        # Threat / Abuse
        "illi baa kuthko", "ninna oddhu haktini",
        "mat aadbeda bai muchu", "nillu hege heliddo hage madu",
        "police ge helidre ide ninge", "Sumne bidalla ninna",

        # Harassment
        "hudugi illi baa", "nan jote bartiya", "phone kodi", "mane yelli",
        "nan jote barbeku"
    ],

    "hindi": [
        # Distress
        "madad karo", "please help", "bachao mujhe", "meri help karo",
        "mujhe bachao", "dar lag raha hai", "mujhe dar lagta hai",

        # Threat / Abuse
        "maar dunga", "chodunga nahi", "idhar aa", "phone de",
        "police ko bataya toh dekh lena",

        # Harassment
        "idhar aao", "kaha ja rahi ho", "mere saath chalo",
        "baat karna hai", "thoda ruk jao"
    ],

    "tamil": [
        # Distress
        "udavi pannunga", "enaku help venum", "kappathunga", "ennai vidunga",
        "enaku payamaga irukku",

        # Threat / Abuse
        "adiyala poduven", "kolre", "intha pakkam vaa", "phone kudu",
        "policuku solra",

        # Harassment
        "ingu vaa", "enga pora", "en kooda vaa", "pesanum",
        "konjam iru"
    ],

    "telugu": [
        # Distress
        "naku help cheyyandi", "dayachesi nannu kapadandi",
        "naku bhayam vestondi", "nannu vadileyandi",

        # Threat / Abuse
        "champutha", "kotesta", "ikkada raa", "phone ivvu",
        "police ki chepta",

        # Harassment
        "ikkada ra", "ekkada velthunnavu", "naatho raa", "koncham nilu"
    ],

    "malayalam": [
        # Distress
        "ente sahayam venam", "enne rakshikkanam", "enikku bhayamund",
        "dayavaayi sahayikku", "enne vida",

        # Threat / Abuse
        "kollo", "adichu kollam", "ivide vaa", "phone tharo",
        "police parayum",

        # Harassment
        "evide pokunnu", "ente koode vaa", "chumma nilkku"
    ],

    "marathi": [
        # Distress
        "mala madat kara", "mala vachva", "mala bhiti vattee",
        "krupa karun madat kara",

        # Threat / Abuse
        "maarun takin", "chodnar nahi", "idhar ye", "phone de",
        "police la sangto",

        # Harassment
        "kuthe chalali", "maze sobat ya", "zara thamba"
    ],

    "english": [
        # Distress
        "help", "help me", "please help", "save me", "i’m scared",
        "i’m in danger", "don’t touch me", "leave me",

        # Threat / Abuse
        "i will kill you", "come here", "give me your phone",
        "don’t move", "shut up",

        # Harassment
        "come with me", "where are you going", "stay with me",
        "stop there"
    ],

    "bengali": [
        # Distress
        "amake bachao", "amake help koro", "amar bhoy lagche",
        "amake chere dao",

        # Threat / Abuse
        "mere felbo", "ekhane esho", "phone dao",
        "police e bole debo",

        # Harassment
        "kothay jachho", "amar sathe eso", "ekto daro"
    ],

    "odia": [
        # Distress
        "mo ku sahajya kar", "mate bachao", "mote bhaya laguchi",

        # Threat / Abuse
        "maridebi", "ethaku aa", "phone de",
        "police ku kahibi",

        # Harassment
        "kouthi jauchu", "mora sathe aasa", "jhada rah"
    ],

    "punjabi": [
        # Distress
        "meri madad karo", "menu bachao", "main darr gayi haan",
        "menu chaddo", "kirpa karke help karo",

        # Threat / Abuse
        "main maar dunga", "idhar aa", "phone de",
        "police nu das dia",

        # Harassment
        "kithe ja rahi ae", "mere naal aa", "thoda rukko"
    ],
}



def detect_abusive(text: str) -> bool:
    lowered = text.lower()
    return any(k in lowered for k in MULTILINGUAL_DANGER_PHRASES)


def map_sentiment_to_emotion(label: str) -> str:
    """
    Convert sentiment label (e.g. "1 star") into a rough emotion.
    1–2 stars: fear / panic
    3 stars: neutral
    4–5 stars: calm
    """
    if "1" in label:
        return "panic"
    if "2" in label:
        return "fear"
    if "3" in label:
        return "neutral"
    if "4" in label or "5" in label:
        return "calm"
    return "neutral"


def map_to_danger_level(stars_label: str, abusive: bool) -> str:
    """
    Convert sentiment + abusive flag into danger level.
    """
    if abusive:
        return "high"

    if "1" in stars_label:
        return "high"
    if "2" in stars_label:
        return "medium"
    if "3" in stars_label:
        return "low"
    # 4 or 5 stars => mostly positive/calm conversation
    return "none"


def classify_transcript(transcript: str) -> dict:
    """
    Classify transcript text into a safety / emotion summary.
    """

    if not transcript or transcript.startswith("[No speech"):
        return {
            "danger_level": "none",
            "emotion": "neutral",
            "has_abusive_keywords": False,
            "reason": "No clear speech detected in audio.",
        }

    # 1) Sentiment analysis (multilingual)
    try:
        sentiment = sentiment_model(transcript[:512])[0]  # first 512 chars
        stars_label = sentiment["label"]  # e.g. "1 star"
    except Exception:
        stars_label = "3 stars"

    # 2) Abusive keyword scan
    abusive = detect_abusive(transcript)

    # 3) Map to emotion & danger level
    emotion = map_sentiment_to_emotion(stars_label)
    danger_level = map_to_danger_level(stars_label, abusive)

    # 4) Reason text
    reason_parts = [f"Sentiment label = {stars_label}."]
    if abusive:
        reason_parts.append("Abusive / threat-like words detected in the transcript.")
    else:
        reason_parts.append("No strong abusive or threat keywords found.")
    reason = " ".join(reason_parts)

    return {
        "danger_level": danger_level,
        "emotion": emotion,
        "has_abusive_keywords": abusive,
        "reason": reason,
    }

# styles.py

def load_dark_theme():
    return """
    <style>

    /* GLOBAL DARK BACKGROUND */
    .stApp {
        background: #0a0f1c;
        color: #e5e7eb;
        font-family: "Segoe UI", sans-serif;
    }

    /* Smooth scroll */
    html { scroll-behavior: smooth; }

    /* FLOATING NAVBAR */
    #floating-nav {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(15, 23, 42, 0.82);
        padding: 10px 22px;
        border-radius: 16px;
        border: 1px solid rgba(56, 189, 248, 0.35);
        display: flex;
        gap: 26px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        backdrop-filter: blur(18px);
        z-index: 9999;
        transition: 0.25s ease;
    }
    #floating-nav a {
        color: #cbd5e1 !important;
        text-decoration: none;
        font-size: 0.92rem;
        font-weight: 500;
        padding: 4px 10px;
        border-radius: 8px;
        transition: 0.25s ease;
    }
    #floating-nav a:hover {
        color: #38bdf8 !important;
        background: rgba(56,189,248,0.12);
        transform: translateY(-2px);
    }

    /* ACTIVE PAGE HIGHLIGHT */
    .active-link {
        color: #38bdf8 !important;
        border-bottom: 2px solid #38bdf8;
    }

    /* CARD CONTAINERS */
    .card {
        background: rgba(15, 23, 42, 0.88);
        border-radius: 18px;
        padding: 20px 25px;
        border: 1px solid rgba(56,189,248,0.35);
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        backdrop-filter: blur(12px);
        transition: 0.28s ease;
    }
    .card:hover {
        transform: translateY(-3px);
        border-color: rgba(56,189,248,0.75);
    }

    /* NEON HEADINGS */
    .title {
        font-size: 1.9rem;
        font-weight: 750;
        color: #e2e8f0;
        text-shadow: 0 0 12px rgba(56,189,248,0.55);
        margin-bottom: 6px;
    }
    .subtitle {
        color: #94a3b8;
        font-size: 0.90rem;
        margin-bottom: 18px;
    }

    /* BUTTONS */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1d4ed8 0%, #0ea5e9 50%, #020617 100%);
        border-radius: 12px;
        color: white;
        padding: 10px;
        border: 1px solid rgba(56,189,248,0.55);
        transition: 0.2s ease;
        font-weight: 600;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(37,99,235,0.6);
        border-color: rgba(191,219,254,1);
    }

    </style>
    """

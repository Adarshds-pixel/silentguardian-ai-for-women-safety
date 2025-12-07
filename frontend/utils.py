# utils.py

import streamlit as st
from styles import load_dark_theme

PAGES = {
    "Home": "Home",
    "Safe Walk": "SafeWalk",
    "Live Analysis": "Analysis",
    "Evidence": "Evidence",
    "How It Works": "HowItWorks",
}

def init_page(page_name):
    """Load global CSS + navbar."""
    st.markdown(load_dark_theme(), unsafe_allow_html=True)
    draw_navbar(page_name)

def draw_navbar(active_page):
    """Floating navbar rendered at top-center."""
    nav_html = '<div id="floating-nav">'
    for name, file in PAGES.items():
        cls = "active-link" if name == active_page else ""
        nav_html += f'<a class="{cls}" href="/{file}">{name}</a>'
    nav_html += "</div>"
    st.markdown(nav_html, unsafe_allow_html=True)

import streamlit as st

def inject_theme():
    st.markdown("""
    <style>
    :root {
        --primary-color: var(--primary-color);
        --background-color: var(--background-color);
        --secondary-background-color: var(--secondary-background-color);
        --text-color: var(--text-color);
    }

    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    div[data-testid="stAppViewContainer"] {
        background-color: var(--background-color);
    }

    section[data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
    }

    .stMarkdown,
    p,
    span,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    label {
        color: var(--text-color);
    }

    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
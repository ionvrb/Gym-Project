# ✅ app.py background & animated text styling
import requests
from streamlit.components.v1 import html
import streamlit as st
import base64
import time
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
                        url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        section[data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .fade-text {{
    font-size: 3.5em;  /* Removed !important */
    font-weight: bold;
    color: #ffffff;
    animation: fadein 2s ease-in-out forwards;
    opacity: 0;
    text-align: left;
    margin: 400px auto 0 5%;
    white-space: normal;
    line-height: 1.2;
}}

        .fade-text-small {{
            font-size: 2.2em;
            color: #ffffff;
            animation: fadein 2s ease-in-out forwards;
            opacity: 0;
            text-align: left;
            margin-left: 5%;
            margin-top: 30px;
        }}

        @keyframes fadein {{
            from {{ opacity: 0; transform: translateY(-10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# ✅ Usage in your app page (call early)
set_bg("assets/app.jpg")

st.markdown("<h1 style='color:white;'>🏋️ Welcome to the GYM Dashboard</h1>", unsafe_allow_html=True)
st.markdown("🔍 Explore scheduled lessons, instructor availability, and course details in a modern and dynamic interface.")
st.markdown("📊 Monitor class distribution across the week")
st.markdown("📝 Add or view lessons, courses, and instructors with ease")

# Quote rotator using JavaScript
html("""
<div id="quote" style="
    padding-top: 2rem;
    font-size: 1.5rem;
    color: #f2f2f2;
    opacity: 1;
    transition: opacity 1s ease-in-out;
    ">
</div>

<script>
  const quotes = [
    "💪 Push yourself, because no one else is going to do it for you.",
    "🔥 The pain you feel today will be the strength you feel tomorrow.",
    "🏋️‍♂️ Train insane or remain the same.",
    "🧠 Motivation gets you started. Habit keeps you going.",
    "⏱️ No excuses. Just results."
  ];

  let i = 0;
  const quoteDiv = document.getElementById("quote");

  function rotateQuote() {
    quoteDiv.style.opacity = 0;
    setTimeout(() => {
      quoteDiv.innerText = quotes[i % quotes.length];
      quoteDiv.style.opacity = 1;
      i++;
    }, 1000);  // Match this to transition time
  }

  rotateQuote();
  setInterval(rotateQuote, 4000);  // Give time for fade-out, text swap, and fade-in
</script>
""", height=100)
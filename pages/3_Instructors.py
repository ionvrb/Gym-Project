import streamlit as st
import pandas as pd
import datetime
import base64
from db_connection import get_connection
from streamlit_lottie import st_lottie
import requests

# ==========
# Background Setup
# ==========
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
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
        </style>
    """, unsafe_allow_html=True)

set_bg("assets/instructors.jpg")

# ==========
# Lottie Animation (Optional)
# ==========
def load_lottie_url(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_json = load_lottie_url("https://lottie.host/7cd2d44e-35c3-4397-90ef-31769b5fa1b7/xfdh7T07RM.json")

col1, col2 = st.columns([1, 4])
with col1:
    if lottie_json:
        st_lottie(lottie_json, height=100)
with col2:
    st.markdown("## 👩‍🏫 Instructor Directory")
    st.markdown("Filter and explore instructor profiles by name, email, or birth date.")

# ==========
# Connect to DB and Prepare Filters
# ==========
conn = get_connection()

st.markdown("### 🔍 Filter Instructors")

surname_filter = st.text_input("Surname starts with:")
email_filter = st.text_input("Email contains (optional):")

min_date = datetime.date(1950, 1, 1)
max_date = datetime.date.today()
date_range = st.date_input("Birthdate Range:", value=[min_date, max_date], min_value=min_date, max_value=max_date)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.info("Please select a valid date range.")
    st.stop()

if start_date == end_date:
    st.info("Please select a date range, not just one day.")
    st.stop()

# ==========
# SQL Query Execution
# ==========
query = """
SELECT * FROM INSTRUCTOR
WHERE Surname LIKE %s
AND BirthDate BETWEEN %s AND %s
"""
params = [f"{surname_filter}%", str(start_date), str(end_date)]

if email_filter:
    query += " AND Email LIKE %s"
    params.append(f"%{email_filter}%")

query += " ORDER BY Surname"

df = pd.read_sql(query, conn, params=params)

# ==========
# Results Display
# ==========
if df.empty:
    st.warning("No instructors match your filters.")
else:
    st.success(f"✅ Found {len(df)} instructor(s)")

    st.markdown("### 🧑‍🏫 Instructor Profiles")
    cols = st.columns(2)

    for idx, (_, row) in enumerate(df.iterrows()):
        avatar_url = f"https://api.dicebear.com/7.x/initials/svg?seed={row['Name']}{row['Surname']}"

        with cols[idx % 2]:
            st.markdown(f"""
            <div style='background-color:#111; padding: 15px; margin-bottom: 10px; border-radius: 10px; border: 1px solid #333; display: flex; align-items: center;'>
                <img src="{avatar_url}" style="width: 60px; height: 60px; border-radius: 50%; margin-right: 15px;">
                <div>
                    <h4 style='color:#FFD700; margin-bottom: 5px;'>🎓 {row['Name']} {row['Surname']}</h4>
                    <p style='color:white; margin: 2px 0;'>📧 <b>Email:</b> {row['Email']}</p>
                    <p style='color:white; margin: 2px 0;'>📞 <b>Phone:</b> {row['Telephone']}</p>
                    <p style='color:white; margin: 2px 0;'>🎂 <b>Birth Date:</b> {row['BirthDate']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
import pandas as pd
import streamlit as st
import mysql.connector
import base64
from db_connection import get_connection

st.title("🗓️ Add New Scheduled Lesson")

conn = get_connection()

# Fetch dropdown options from DB
instructors = pd.read_sql("SELECT FisCode FROM INSTRUCTOR", conn)
courses = pd.read_sql("SELECT CodC FROM COURSES", conn)

# ========== Form ==========
with st.form("add_program_form"):
    fiscode = st.selectbox("Select Instructor (FisCode)", instructors['FisCode'])
    day = st.selectbox("Day of the Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    start_time = st.slider("Start Time (24h format)", min_value=6, max_value=21, step=1)
    duration = st.slider("Duration (minutes)", min_value=15, max_value=60, step=15)
    codc = st.selectbox("Select Course (CodC)", courses['CodC'])
    room = st.text_input("Room")

    submitted = st.form_submit_button("Add Lesson")

    if submitted:
        if not all([fiscode, day, start_time, duration, codc, room]):
            st.error("❗ All fields are required.")
        elif duration > 60:
            st.error("❗ Duration cannot exceed 60 minutes.")
        else:
            try:
                # Check for conflict
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM PROGRAM WHERE CodC = %s AND Day = %s",
                    (codc, day)
                )
                conflict = cursor.fetchone()
                if conflict:
                    st.error("❌ A lesson for this course already exists on that day.")
                else:
                    # Insert into PROGRAM
                    cursor.execute(
                        "INSERT INTO PROGRAM (FisCode, Day, StartTime, Duration, CodC, Room) VALUES (%s, %s, %s, %s, %s, %s)",
                        (fiscode, day, start_time, duration, codc, room)
                    )
                    conn.commit()
                    st.success("✅ Lesson added successfully.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}") 
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)),
                    url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* 🧊 Frosted Glass Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}
    </style>
    """,
    unsafe_allow_html=True
)
set_bg("assets/addlesson.jpg")
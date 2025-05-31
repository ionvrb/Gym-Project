import streamlit as st
import base64
import mysql.connector
from db_connection import get_connection

st.title("➕ Add New Course")

# ========== Form ==========
with st.form("add_course_form"):
    codc = st.text_input("Course Code (e.g., CT005)")
    name = st.text_input("Course Name")
    ctype = st.text_input("Course Type (e.g., Yoga, Cardio)")
    level = st.number_input("Level (1 to 4)", min_value=1, max_value=4, step=1)

    submitted = st.form_submit_button("Add Course")

    if submitted:
        # ===== Validations =====
        if not all([codc, name, ctype]):
            st.error("❗ All fields are required.")
        elif not codc.startswith("CT"):
            st.error("❗ Course code must start with 'CT'.")
        else:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO COURSES (CodC, Name, CType, Level) VALUES (%s, %s, %s, %s)",
                    (codc, name, ctype, level)
                )
                conn.commit()
                st.success(f"✅ Course '{name}' added successfully!")
            except mysql.connector.IntegrityError:
                st.error("❌ A course with that code already exists.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
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
set_bg("assets/addcourse.jpg")
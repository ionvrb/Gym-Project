import streamlit as st
import pandas as pd
import base64
from db_connection import get_connection
from streamlit_lottie import st_lottie
import requests

# ==========
# Lottie Loader (Optional Animation)
# ==========
def load_lottie_url(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_course = load_lottie_url("https://assets9.lottiefiles.com/private_files/lf30_rpg3g4ba.json")

# ==========
# Page Title and Lottie Animation
# ==========
col1, col2 = st.columns([1, 4])
with col1:
    if lottie_course:
        st_lottie(lottie_course, height=100)
with col2:
    st.markdown("## 📚 Browse Available Courses")
    st.markdown("Use filters below to explore courses by type, level, or name.")

# ==========
# Connect to DB
# ==========
conn = get_connection()
df_courses = pd.read_sql("SELECT * FROM courses", conn)

# ==========
# Filters UI
# ==========
st.markdown("### 🔍 Filter Courses")

course_types = df_courses['CType'].unique().tolist()
min_level = int(df_courses['Level'].min())
max_level = int(df_courses['Level'].max())

with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        search_name = st.text_input("Search by Course Name:")
    with col2:
        selected_level = st.slider("Level Range:", min_value=min_level, max_value=max_level, value=(min_level, max_level))

selected_types = st.multiselect("Filter by Course Type:", options=course_types, default=course_types)

# ==========
# Apply Filters
# ==========
filtered = df_courses[
    df_courses['CType'].isin(selected_types) &
    df_courses['Level'].between(selected_level[0], selected_level[1]) &
    df_courses['Name'].str.contains(search_name, case=False)
]

# ==========
# Metrics Display
# ==========
st.markdown("### 📈 Course Stats")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"#### 🎯 Total Courses: `{len(filtered)}`")
with col2:
    st.markdown(f"#### 🧬 Unique Types: `{df_courses['CType'].nunique()}`")

# ==========
# Display Filtered Courses as Cards
# ==========
if filtered.empty:
    st.warning("No courses match the selected filters.")
else:
    st.markdown("### 🗂️ Matching Courses")
    for _, row in filtered.iterrows():
        st.markdown(f"""
        <div style='background-color: #111; padding: 15px; margin-bottom: 10px; border-radius: 12px; border: 1px solid #333;'>
            <h4 style='color:#FFD700;'>🏋️ {row['Name']}</h4>
            <p style='color:white;'>📦 Type: <b>{row['CType']}</b> | 🎚️ Level: <b>{row['Level']}</b></p>
            <p style='color:#ccc;'>🆔 Course Code: {row['CodC']}</p>
        </div>
        """, unsafe_allow_html=True)

    # ==========
    # Expander: Lesson Plan + Instructor Info
    # ==========
    with st.expander("📅 Show Lesson Plan + Instructors for These Courses"):
        course_codes = tuple(filtered['CodC'])
        query = f"""
        SELECT P.CodC, P.Day, P.StartTime, P.Room,
               CONCAT(I.Name, ' ', I.Surname) AS Instructor,
               I.Email
        FROM program P
        JOIN instructor I ON P.FisCode = I.FisCode
        WHERE P.CodC IN {course_codes if len(course_codes) > 1 else f"('{course_codes[0]}')"}
        ORDER BY P.CodC, P.Day, P.StartTime;
        """

        df_lessons = pd.read_sql(query, conn)

        if df_lessons.empty:
            st.info("No scheduled lessons for selected courses.")
        else:
            df_lessons = df_lessons.rename(columns={
                "CodC": "Course Code",
                "Day": "Day",
                "StartTime": "Start Time",
                "Room": "Room",
                "Instructor": "Instructor",
                "Email": "Instructor Email"
            })
            st.dataframe(df_lessons, use_container_width=True)
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
set_bg("assets/courses.jpg")
import streamlit as st
import pandas as pd
import altair as alt
import base64
import mysql.connector
from db_connection import get_connection

st.title("🏠 GYM Dashboard")
st.markdown("### Overview of Scheduled Lessons in the Week")

conn = get_connection()
df = pd.read_sql("SELECT Day, StartTime FROM PROGRAM", conn)

# Metric: Total lessons
st.metric("📅 Total Lessons", len(df))

# Compute time and day counts
time_counts = df['StartTime'].value_counts().sort_index()
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
day_counts = df['Day'].value_counts().reindex(day_order).fillna(0)

# Chart dataframes
bar_df = time_counts.reset_index()
bar_df.columns = ['StartTime', 'Count']

line_df = day_counts.reset_index()
line_df.columns = ['Day', 'Count']

alt.themes.enable('none')  # make sure Altair doesn’t override with dark bg

# Layout in two columns
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("⏰ Lessons by Time Slot")
    bar_chart = alt.Chart(bar_df).mark_bar().encode(
        x=alt.X('StartTime:O', title='Hour of Day', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Count:Q', title='Number of Lessons'),
        tooltip=['StartTime', 'Count']
    ).properties(width=500, height=300
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        grid=False,
        domain=False,
        labelColor='white',
        titleColor='white'
    ).configure(
        background='transparent'
    )
    st.altair_chart(bar_chart)

with col2:
    st.subheader("📅 Lessons by Day of Week")
    line_chart = alt.Chart(line_df).mark_line(point=True).encode(
        x=alt.X('Day:O', sort=day_order, axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Count:Q'),
        tooltip=['Day', 'Count']
    ).properties(width=400, height=300
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        grid=False,
        domain=False,
        labelColor='white',
        titleColor='white'
    ).configure(
        background='transparent'
    )
    st.altair_chart(line_chart)

# Optional: Pie Chart for % by Day
with st.expander("📊 Lesson Distribution by Day (Pie Chart)"):
    pie_df = line_df.copy()

    pie_chart = alt.Chart(pie_df).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field='Count', type='quantitative'),
        color=alt.Color(field='Day', type='nominal'),
        tooltip=['Day', 'Count']
    ).properties(
        width=400,
        height=400
    ).configure_view(
        strokeWidth=0
    ).configure_legend(
        labelColor='white',
        titleColor='white'
    ).configure(
        background='transparent'
    )

    st.altair_chart(pie_chart, use_container_width=True)
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
set_bg("assets/homepage.jpeg")
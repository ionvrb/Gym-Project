import mysql.connector
import streamlit as st
@st.cache_resource
def get_connection():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["db_host"],
            port=int(st.secrets["db_port"]),
            user=st.secrets["db_user"],
            password=st.secrets["db_password"],
            database=st.secrets["db_name"],
            connect_timeout=10  # ⏳ Prevents infinite loading
        )
        return conn
    except Exception as e:
        st.error(f"❌ DB connection failed: {e}")
        raise
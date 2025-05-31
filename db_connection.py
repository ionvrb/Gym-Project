import mysql.connector
import streamlit as st

@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="epistulaeexponto03",  # your MySQL password
        database="GYM"
    ) 

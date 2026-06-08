import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_connection

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first!")
    if st.button("Go to Login"):
        st.switch_page("pages/0_Login.py")
    st.stop()

st.title("👗 My Outfit History")
st.subheader(f"All your past outfit suggestions, {st.session_state.username}!")

st.markdown("---")

try:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT city, occasion, suggestion, created_at 
        FROM outfit_history 
        WHERE user_id = %s 
        ORDER BY created_at DESC
    """, (st.session_state.user_id,))
    
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if not history:
        st.info("No outfit history yet! Go to the OOTD Assistant and get your first suggestion! 👗")
    else:
        for i, (city, occasion, suggestion, created_at) in enumerate(history):
            with st.expander(f"👗 {occasion} outfit for {city} — {created_at.strftime('%B %d, %Y')}"):
                st.write(suggestion)

except Exception as e:
    st.error(f"Error loading history: {e}")
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import register_user, login_user

st.set_page_config(
    page_title="StyleSync - Login",
    page_icon="👗",
    layout="centered"
)

st.title("👗 StyleSync")
st.subheader("Your Personal AI Style Assistant")

st.markdown("---")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None

if st.session_state.logged_in:
    st.success(f"Welcome back, {st.session_state.username}!! 👋")
    if st.button("Go to OOTD Assistant"):
        st.switch_page("pages/1_OOTD_Assistant.py")
    if st.button("Go to Fashion Analytics"):
        st.switch_page("pages/2_Fashion_Analytics.py")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.rerun()
else:
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.markdown("### Welcome Back! 👋")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_btn"):
            if not username or not password:
                st.warning("Please fill in all fields!")
            else:
                user_id = login_user(username, password)
                if user_id:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.success(f"Welcome back, {username}!! 🎉")
                    st.rerun()
                else:
                    st.error("Invalid username or password!")
    
    with tab2:
        st.markdown("### Create Your Account! ✨")
        new_username = st.text_input("Choose a Username", key="reg_username")
        new_email = st.text_input("Email Address", key="reg_email")
        new_password = st.text_input("Choose a Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Create Account", key="register_btn"):
            if not new_username or not new_email or not new_password or not confirm_password:
                st.warning("Please fill in all fields!")
            elif new_password != confirm_password:
                st.error("Passwords don't match!")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters!")
            else:
                success = register_user(new_username, new_email, new_password)
                if success:
                    st.success("Account created successfully! Please login! 🎉")
                else:
                    st.error("Username or email already exists!")
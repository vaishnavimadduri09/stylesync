import streamlit as st

st.set_page_config(
    page_title="StyleSync",
    page_icon="👗",
    layout="wide"
)

# Check if user is logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("👗 StyleSync")
    st.subheader("Your Personal AI Style Assistant")
    st.markdown("---")
    st.info("Please login or create an account to continue!")
    if st.button("Go to Login / Sign Up"):
        st.switch_page("pages/0_Login.py")
else:
    st.title(f"👗 StyleSync")
    st.subheader(f"Welcome, {st.session_state.username}!! 🌟")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.info("### 👗 OOTD Assistant\nUpload your clothes and get a personalized outfit suggestion based on weather, occasion and trends!")
        if st.button("Go to OOTD Assistant"):
            st.switch_page("pages/1_OOTD_Assistant.py")

    with col2:
        st.info("### 📊 Fashion Analytics\nExplore global fashion trends, popular styles and what people are wearing around the world!")
        if st.button("Go to Fashion Analytics"):
            st.switch_page("pages/2_Fashion_Analytics.py")

    st.markdown("---")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.rerun()

    st.caption("Built with Python, Streamlit, Claude AI and OpenWeather API")
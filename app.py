import streamlit as st

st.set_page_config(
    page_title="OOTD Intelligence Platform",
    page_icon="👗",
    layout="wide"
)

st.title("👗 OOTD Intelligence Platform")
st.subheader("Your Personal AI Wardrobe Assistant & Fashion Analytics Dashboard")

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
st.caption("Built with Python, Streamlit, Google Gemini AI and Weather API")
import streamlit as st
import anthropic
import requests
import os
import base64
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

# Support both local .env and Streamlit Cloud secrets
if "WEATHER_API_KEY" in st.secrets:
    os.environ["WEATHER_API_KEY"] = st.secrets["WEATHER_API_KEY"]
if "ANTHROPIC_API_KEY" in st.secrets:
    os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

st.title("👗 OOTD Assistant")
st.subheader("Upload your clothes and get a personalized outfit suggestion!")

col1, col2 = st.columns(2)

with col1:
    city = st.text_input("📍 Enter your city:", placeholder="e.g. Mumbai, London, New York")

with col2:
    occasion = st.selectbox("👔 Select your occasion:", 
    ["Casual", "Work", "Party", "Date", "Gym", "Formal"])

st.markdown("### 📸 Upload photos of your clothes")
uploaded_files = st.file_uploader(
    "Upload your clothing items",
    accept_multiple_files=True,
    type=["jpg", "jpeg", "png"]
)

if uploaded_files:
    st.markdown("### Your uploaded clothes:")
    cols = st.columns(len(uploaded_files))
    for i, file in enumerate(uploaded_files):
        with cols[i]:
            img = Image.open(file)
            st.image(img, caption=f"Item {i+1}", width=200)

if st.button("✨ Get My Outfit Suggestion!"):
    if not city:
        st.warning("Please enter your city!")
    elif not uploaded_files:
        st.warning("Please upload at least one clothing item!")
    else:
        with st.spinner("Analyzing your wardrobe and checking the weather..."):
            weather_api_key = os.getenv("WEATHER_API_KEY")
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()

            if weather_response.status_code == 200:
                temp = weather_data["main"]["temp"]
                description = weather_data["weather"][0]["description"]
                
                st.success(f"🌤️ Weather in {city}: {temp}°C, {description}")
                
                image_contents = []
                for file in uploaded_files:
                    img_bytes = file.getvalue()
                    img_base64 = base64.standard_b64encode(img_bytes).decode("utf-8")
                    file_type = file.type if file.type else "image/jpeg"
                    image_contents.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": file_type,
                            "data": img_base64
                        }
                    })
                
                image_contents.append({
                    "type": "text",
                    "text": f"""You are a professional fashion stylist. 
                    The user is in {city} where it is currently {temp}°C and {description}.
                    They are dressing for a {occasion} occasion.
                    Looking at their clothing items in the images, suggest the best outfit combination.
                    Be specific about which items to combine and why.
                    Also suggest how to accessorize.
                    Keep it friendly and encouraging!"""
                })
                
                try:
                    response = client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=1024,
                        messages=[
                            {"role": "user", "content": image_contents}
                        ]
                    )
                    st.markdown("### ✨ Your Outfit Suggestion:")
                    st.write(response.content[0].text)
                except Exception as e:
                    st.error(f"AI Error: {e}")
            else:
                st.error(f"City not found! Please check the city name. Debug: {weather_data}")

st.markdown("---")
st.markdown("### 🌍 Trending Outfits for Inspiration")

trends = {
    "Casual": ["Oversized blazer + straight leg jeans", "Linen co-ord sets", "Chunky sneakers + cargo pants"],
    "Work": ["Tailored trousers + fitted blazer", "Midi skirt + tucked in blouse", "Monochrome suits"],
    "Party": ["Sequin mini dress", "Satin slip dress + heels", "Bold colored jumpsuit"],
    "Date": ["Wrap dress + strappy heels", "Smart casual blazer + fitted trousers", "Flowy midi dress"],
    "Gym": ["High waist leggings + sports bra", "Matching tracksuit", "Oversized tee + biker shorts"],
    "Formal": ["Classic suit", "Floor length gown", "Tailored dress + blazer"]
}

for trend in trends[occasion]:
    st.markdown(f"- 👗 {trend}")
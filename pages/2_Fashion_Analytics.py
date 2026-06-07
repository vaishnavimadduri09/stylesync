import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Fashion Analytics Dashboard")
st.subheader("Global Fashion Trends & Insights")

# Sample fashion trend data
data = {
    "Country": ["USA", "UK", "France", "Italy", "Japan", "India", "Australia", "Brazil", "Germany", "South Korea"],
    "Casual_Wear": [85, 78, 72, 68, 90, 75, 88, 80, 76, 92],
    "Formal_Wear": [45, 55, 65, 70, 40, 60, 42, 38, 58, 35],
    "Streetwear": [90, 75, 70, 65, 95, 60, 72, 78, 68, 98],
    "Sustainable_Fashion": [65, 70, 80, 75, 60, 45, 72, 50, 82, 55],
    "Luxury_Fashion": [55, 60, 85, 90, 65, 50, 52, 45, 58, 70]
}

df = pd.DataFrame(data)

st.markdown("---")

# Section 1 - Trending styles by country
st.markdown("### 🌍 Trending Styles by Country")
selected_style = st.selectbox(
    "Select a fashion style:",
    ["Casual_Wear", "Formal_Wear", "Streetwear", "Sustainable_Fashion", "Luxury_Fashion"]
)

fig1 = px.bar(
    df,
    x="Country",
    y=selected_style,
    color="Country",
    title=f"{selected_style.replace('_', ' ')} Popularity by Country",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# Section 2 - Fashion radar chart
st.markdown("### 📊 Fashion Style Comparison")
selected_countries = st.multiselect(
    "Select countries to compare:",
    df["Country"].tolist(),
    default=["USA", "France", "Japan"]
)

if selected_countries:
    filtered_df = df[df["Country"].isin(selected_countries)]
    melted_df = filtered_df.melt(
        id_vars="Country",
        var_name="Style",
        value_name="Popularity"
    )
    fig2 = px.line_polar(
        melted_df,
        r="Popularity",
        theta="Style",
        color="Country",
        line_close=True,
        title="Fashion Style Radar Chart",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Section 3 - Trending colors this season
st.markdown("### 🎨 Trending Colors This Season")

colors_data = {
    "Color": ["Sage Green", "Butter Yellow", "Cobalt Blue", "Terracotta", "Lavender", "Off White", "Rust Orange", "Navy"],
    "Trend_Score": [92, 88, 85, 83, 80, 78, 75, 72],
    "Hex": ["#8faa8b", "#f5e642", "#0047ab", "#c66c3a", "#967bb6", "#faf0e6", "#c45e2a", "#000080"]
}

colors_df = pd.DataFrame(colors_data)

fig3 = px.bar(
    colors_df,
    x="Trend_Score",
    y="Color",
    orientation="h",
    title="Top Trending Colors This Season",
    color="Color",
    color_discrete_sequence=colors_df["Hex"].tolist()
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# Section 4 - Key insights
st.markdown("### 💡 Key Fashion Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌍 Top Streetwear Country", "South Korea", "+98%")

with col2:
    st.metric("♻️ Most Sustainable Country", "Germany", "+82%")

with col3:
    st.metric("👑 Luxury Fashion Capital", "Italy", "+90%")
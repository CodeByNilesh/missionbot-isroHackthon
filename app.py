import streamlit as st
import os
import requests
from dotenv import load_dotenv
from chatbot_engine import (
    load_knowledge_base,
    build_faiss_index,
    search_answer
)
from streamlit_folium import st_folium
import folium

# 🔐 Load API key
load_dotenv()

# 🧠 Load and embed knowledge base
questions, answers = load_knowledge_base()
model, index, embeddings = build_faiss_index(questions)

# 🌐 Geocoding for coordinates
def get_coordinates(city_name):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    try:
        res = requests.get(geo_url)
        data = res.json()
        if data:
            return data[0]["lat"], data[0]["lon"]
    except:
        pass
    return None, None

# 🌫️ AQI fetcher
def get_aqi(lat, lon, city_name):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        aqi_value = data["list"][0]["main"]["aqi"]
        levels = {
            1: "Good", 2: "Fair", 3: "Moderate",
            4: "Poor", 5: "Very Poor"
        }
        return f"AQI in {city_name}: {aqi_value} – {levels.get(aqi_value, 'Unknown')}"
    except:
        return "⚠️ AQI data is unavailable."

# 🌦️ Weather fetcher
def get_weather(lat, lon, city_name):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"].title()
        humidity = data["main"]["humidity"]
        return f"Weather in {city_name}: {temp}°C, {condition}, Humidity: {humidity}%"
    except:
        return "❌ Weather data is unavailable."

# 🚀 UI setup
st.set_page_config(page_title="MissionBot 🚀", layout="centered")
st.title("MissionBot: Space + Real-Time City Assistant")
st.caption("Ask questions or explore live environmental data from any city 🌍")

# 📂 Tabs for Chat and City Explorer
tab1, tab2 = st.tabs(["💬 Ask MissionBot", "🏙️ City Explorer"])

with tab1:
    user_query = st.text_input("What would you like to know about space ?")
    if user_query:
        response = search_answer(user_query, model, index, questions, answers, embeddings)
        st.success(response)

with tab2:
    city_name = st.text_input("Enter a city name (e.g. Pune, Delhi):")
    if city_name:
        lat, lon = get_coordinates(city_name)
        if lat and lon:
            st.info(get_aqi(lat, lon, city_name))
            st.success(get_weather(lat, lon, city_name))

            with st.expander("🗺️ Show map location", expanded=False):
                m = folium.Map(location=[lat, lon], zoom_start=10, control_scale=False)
                folium.Marker([lat, lon], popup=city_name.title()).add_to(m)
                st_folium(m, width=700, returned_objects=[])
        else:
            st.error("City not found. Please check the spelling.")

#%% Import Dependencies
import streamlit as st
import functions.user_info as fu
import functions.weather_data as fw
import os
from datetime import datetime

# Get Weather Data API Key
weather_api_key = os.environ.get('weather_api_key')

# Setup app
st.set_page_config(layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Get the user's IP address and location
user_ip = fu.get_ip()
city, region, zipcode, country = fu.get_location(user_ip)

# Fetch Current Weather data for user's location
location = f'{city}, {region}, {zipcode}, {country}'
weather_df, condition_df, aqi_df = fw.current_weather_get(weather_api_key, location)

# App's Current Weather Section
with st.container():
    location_text = f"## {city}, {region}"
    st.write(location_text)
    st.write("Current Conditions")

    img_path = f"https:{condition_df['icon'][0]}"
    st.markdown(
        f"""
        <div style='display: flex; justify-content: center;'>
            <img src='{img_path}' alt='Weather Icon'>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"<p style='padding: 0px;'><b>{condition_df['text'][0]}</b></p>", unsafe_allow_html=True)
    st.markdown(f"""<p style='padding: 0px;'>
                    <b>Temperature:</b> {weather_df['temp_f'][0]}°F <br>
                    <b>Humidity:</b> {weather_df['humidity'][0]}% <br>
                    <b>Wind Speed:</b> {weather_df['wind_mph'][0]} mph
                  </p>""", unsafe_allow_html=True)







# # Fetch Astronomy data for user's location
# location = f'{city}, {region}, {zipcode}, {country}'
# date = datetime.now().strftime('%Y-%m-%d')
# df = fw.astronomy_get(weather_api_key, location, date)

# st.dataframe(df, hide_index=True)


st.dataframe(weather_df, hide_index=True)
st.dataframe(condition_df, hide_index=True)
st.dataframe(aqi_df, hide_index=True)
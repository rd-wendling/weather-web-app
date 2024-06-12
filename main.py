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
st.title('Streamlit Dashboard with IP Capture')

# Get the user's IP address
user_ip = fu.get_ip()

# Display the IP address in the app
st.write(f"Your IP address is: {user_ip}")

# Display the Location in the app
city, region, zipcode, country = fu.get_location(user_ip)
text = f"City: {city}, Region: {region}, Zipcode: {zipcode}, Country: {country}"
st.write(text)

# Fetch Astronomy data for user's location
location = f'{city}, {region}, {zipcode}, {country}'
date = datetime.now()
df = fw.astronomy_get(weather_api_key, location, date)

st.dataframe(df, hide_index=True)


# Fetch Current Weather data for user's location
location = f'{city}, {region}, {zipcode}, {country}'
df = fw.current_weather_get(weather_api_key, location)

st.dataframe(df, hide_index=True)
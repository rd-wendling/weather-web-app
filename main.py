#%% Import Dependencies
import streamlit as st
import functions.user_info as fu
import functions.weather_data as fw
import functions.streamlit_helpers as fs
from datetime import datetime
import base64

# Get Weather Data API Key
weather_api_key = st.secrets["weather_api_key"]

# Setup app
st.set_page_config(layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Handle Small Screens
st.write(f"<p class='error-message'>Display  Error: Screen size is too small!</p>", unsafe_allow_html=True)

# Get the user's IP address and location
user_ip = fu.get_ip()

# Get the user's location
city, region, zipcode, country = fu.get_location(user_ip)
location = f'{city}, {region}, {zipcode}, {country}'


location_text = f"# Location detected as: {city}, {region}"
st.write(location_text)

st.write('')
with st.container():
    location_overide = st.text_input("Overide detected location with zipcode input:")

if location_overide:
    location = location_overide
    
# Fetch Current Weather data for user's location
weather_df, condition_df, aqi_df = fw.current_weather_get(weather_api_key, location)

# Fetch Astronomy data
date = datetime.now().strftime('%Y-%m-%d')
astro_df = fw.astronomy_get(weather_api_key, location, date)

# Fetch 7-Day Forecast
forecast_df = fw.forecast_weather_get(weather_api_key, location, 7)


# App's Current Weather and Astro Section
current_col, astro_col = st.columns([1, 1])
with current_col:
    st.write("## Today's Outlook")
    st.markdown(f"<p style='padding-top: 5px; margin-top:25px;'>Current Conditions</p>", unsafe_allow_html=True)

    img_path = f"https:{condition_df['icon'][0]}"
    st.markdown(
        f"""
        <div style='display: flex; justify-content: center; padding: 0px; margin-top:-10pt;'>
            <img src='{img_path}' alt='Weather Icon'>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"<p style='padding: 0px; margin-bottom:10px; margin-top:-5pt;'><b>{condition_df['text'][0]}</b></p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""<p style='padding: 0px; text-align:left'>
                        <b>Temperature:</b> {weather_df['temp_f'][0]} °F <br>
                        <b>Humidity:</b> {weather_df['humidity'][0]}% <br>
                        <b>Wind Speed:</b> {weather_df['wind_mph'][0]} mph
                    </p>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<p style='padding: 0px; text-align:left; position:absolute; right:0; top:0'>
                        <b>Feels Like:</b> {weather_df['feelslike_f'][0]} °F <br>
                        <b>Visibility:</b> {weather_df['vis_miles'][0]} miles <br>
                        <b>Wind Gusts:</b> {weather_df['gust_mph'][0]} mph
                    </p>""", unsafe_allow_html=True)

with astro_col:
    st.write("## Astronomy")

    # Get todays moon phase and path to right icon
    moon_phase = astro_df[astro_df['index']=='moon_phase']['astro'].reset_index(drop=True)
    st.markdown(f"<p style='padding-top: 5px; margin-top:25px;'>{moon_phase[0]}</p>", unsafe_allow_html=True)
    img_path = fw.get_moon_icon_path(moon_phase[0])

    # Read the image file as bytes
    with open(img_path, "rb") as img_file:
        img_bytes = img_file.read()

    # Encode the image bytes as base64
    img_base64 = base64.b64encode(img_bytes).decode()

    st.markdown(
        f"""
        <div class="image-container">
            <img src="data:image/png;base64,{img_base64}" alt="Image" style="width: 35px;">
        </div>
        """,
        unsafe_allow_html=True
    )

    sunrise = astro_df[astro_df['index']=='sunrise']['astro'].reset_index(drop=True)
    sunset = astro_df[astro_df['index']=='sunset']['astro'].reset_index(drop=True)
    moonrise = astro_df[astro_df['index']=='moonrise']['astro'].reset_index(drop=True)
    moonset = astro_df[astro_df['index']=='moonset']['astro'].reset_index(drop=True)
    moon_illum = astro_df[astro_df['index']=='moon_illumination']['astro'].reset_index(drop=True)

    st.markdown(f"""<p style='padding-top: 10px;'><b>Moon Illumination:</b> {moon_illum[0]}%</p>""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""<p style='padding-top: 5px; text-align:left'>
                        <b>Sun Rise:</b> {sunrise[0]}<br>
                        <b>Sun Set:</b> {sunset[0]}
                    </p>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<p style='padding-top: 5px; text-align:left; position:absolute; right:0; top:0'>
                        <b>Moon Rise:</b> {moonrise[0]}<br>
                        <b>Moon Set:</b> {moonset[0]}
                    </p>""", unsafe_allow_html=True)

# App's Forecast Section
with st.container():
    st.write("### 7-Day Forecast")
    metric, day1, day2, day3, day4, day5, day6, day7 = st.columns(8)
    with metric:
        st.markdown(f"""<p style='text-align: left; padding-top: 40px;'><b></b></p>""", unsafe_allow_html=True)
        st.markdown(f"""<p style='text-align: left; padding-top: 0px;'><b></b></p>""", unsafe_allow_html=True)
        st.markdown(f"""<p style='text-align: left; padding-top: 60px;'><b>High</b></p>""", unsafe_allow_html=True)
        st.markdown(f"""<p style='text-align: left; padding-top: 0px;'><b>Low</b></p>""", unsafe_allow_html=True)
        st.markdown(f"""<p style='text-align: left; padding-top: 0px;'><b>Chance of Rain</b></p>""", unsafe_allow_html=True)
        st.markdown(f"""<p style='text-align: left; padding-top: 0px;'><b>Max Wind Speed</b></p>""", unsafe_allow_html=True)

    with day1:
        col_index = 0
        fs.forecast_column(col_index, forecast_df)
    with day2:
        col_index = 1
        fs.forecast_column(col_index, forecast_df)
    with day3:
        col_index = 2
        fs.forecast_column(col_index, forecast_df)
    with day4:
        col_index = 3
        fs.forecast_column(col_index, forecast_df)
    with day5:
        col_index = 4
        fs.forecast_column(col_index, forecast_df)
    with day6:
        col_index = 5
        fs.forecast_column(col_index, forecast_df)
    with day7:
        col_index = 6
        fs.forecast_column(col_index, forecast_df)




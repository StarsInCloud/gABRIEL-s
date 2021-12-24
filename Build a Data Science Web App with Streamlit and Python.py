import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATE_TIME = "date/time"
DATA_URL = (
    "/path/to/Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("Motor Vehicle Collisions in New York City")
st.markdown("This application is a Streamlit dashboard that can be used "
            "to analyze motor vehicle collisions in NYC 🗽💥🚗")


@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data.rename(columns={"crash_date_crash_time": "date/time"}, inplace=True)
    #data = data[['date/time', 'latitude', 'longitude']]
    return data

data = load_data(15000)
data[['latitude','longitude']].to_csv('lat_long.csv', index=False)


st.header("Where are the most people injured in NYC?")
injured_people = st.slider("Number of persons injured in vehicle collisions", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

st.header("How many collisions occur during a given time of day?")
hour = st.slider("Hour to look at", 0, 23)
original_data = data
data = data[data[DATE_TIME].dt.hour == hour]
st.markdown("Vehicle collisions between %i:00 and %i:00" % (hour, (hour + 1) % 24))

midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
        "Hexago
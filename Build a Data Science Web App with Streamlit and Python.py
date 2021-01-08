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
st.markdown("This applicat
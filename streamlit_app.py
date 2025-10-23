import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Temperature & Humidity Dashboard", page_icon="🌡️")

# -----------------------------------------------------------------------------
# Load data
@st.cache_data
def get_environment_data():
    # 👇 This line finds the CSV inside your repo workspace
    DATA_FILENAME = Path(__file__).parent / "data" / "environment_data.csv"
    df = pd.read_csv(DATA_FILENAME)
    return df

env_df = get_environment_data()

# -----------------------------------------------------------------------------
# Page layout
st.title("🌤️ Temperature and Humidity Over Time")
st.write("This dashboard shows temperature and humidity readings over time.")

st.dataframe(env_df.head())

st.line_chart(env_df, x="Time", y=["Temperature (°C)", "Humidity (%)"])


# -------------------------------------------------------------------------
# Display basic info
st.subheader("Preview of Data")
st.dataframe(df.head())

# -------------------------------------------------------------------------
# Slider to filter by time range
time_min = df["Time"].min()
time_max = df["Time"].max()

time_range = st.slider(
    "Select Time Range",
    min_value=float(time_min),
    max_value=float(time_max),
    value=(float(time_min), float(time_max))
)

filtered_df = df[(df["Time"] >= time_range[0]) & (df["Time"] <= time_range[1])]

# -------------------------------------------------------------------------
# Line chart for temperature and humidity
st.subheader("Temperature and Humidity Over Time")
st.line_chart(
    filtered_df,
    x="Time",
    y=["Temperature (°C)", "Humidity (%)"]
)

# -------------------------------------------------------------------------
# Display some summary stats
st.subheader("Summary Statistics")

col1, col2 = st.columns(2)

with col1:
    st.metric("Average Temperature (°C)", f"{filtered_df['Temperature (°C)'].mean():.1f}")
with col2:
    st.metric("Average Humidity (%)", f"{filtered_df['Humidity (%)'].mean():.1f}")

# Optional: show the code itself
i

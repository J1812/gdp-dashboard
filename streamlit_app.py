import streamlit as st
import pandas as pd
import math
from pathlib import Path

# --------------------------------------------------------------------
# Page setup
st.set_page_config(
    page_title='Temperature & Humidity Dashboard',
    page_icon=':thermometer:',
)

# --------------------------------------------------------------------
# Load data from your CSV
@st.cache_data
def get_environment_data():
    """Read temperature and humidity data from a local CSV file."""

    # 👉 CHANGE THIS PATH to match where you saved your file
    DATA_FILENAME = Path(r"C:\Users\jbell\Downloads\environment_data.csv")

    df = pd.read_csv(DATA_FILENAME)
    df['Date'] = pd.to_datetime(df['Date'])  # ensure date format
    return df

env_df = get_environment_data()

# --------------------------------------------------------------------
# Page title and description
'''
# 🌡️ Temperature & Humidity Dashboard

Visualize temperature and humidity trends over time for selected locations.
'''

# --------------------------------------------------------------------
# Sidebar filters
min_date = env_df['Date'].min().date()
max_date = env_df['Date'].max().date()

from_date, to_date = st.slider(
    'Select date range:',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date],
    format="YYYY-MM-DD"
)

locations = sorted(env_df['Location'].unique())

selected_locations = st.multiselect(
    'Select locations:',
    locations,
    default=locations[:2] if len(locations) >= 2 else locations
)

# --------------------------------------------------------------------
# Filter the data
filtered_df = env_df[
    (env_df['Location'].isin(selected_locations)) &
    (env_df['Date'].between(str(from_date), str(to_date)))
]

# --------------------------------------------------------------------
# Charts
st.header('Temperature over time', divider='gray')
st.line_chart(
    filtered_df,
    x='Date',
    y='Temperature',
    color='Location'
)

st.header('Humidity over time', divider='gray')
st.line_chart(
    filtered_df,
    x='Date',
    y='Humidity',
    color='Location'
)

# --------------------------------------------------------------------
# Metrics summary
st.header('Summary metrics', divider='gray')

cols = st.columns(4)

for i, loc in enumerate(selected_locations):
    col = cols[i % len(cols)]

    with col:
        loc_data = filtered_df[filtered_df['Location'] == loc]

        if not loc_data.empty:
            avg_temp = loc_data['Temperature'].mean()
            avg_hum = loc_data['Humidity'].mean()
            delta_temp = loc_data['Temperature'].iloc[-1] - loc_data['Temperature'].iloc[0]
            delta_hum = loc_data['Humidity'].iloc[-1] - loc_data['Humidity'].iloc[0]
        else:
            avg_temp = avg_hum = delta_temp = delta_hum = float('nan')

        st.metric(
            label=f'{loc} Avg Temp (°C)',
            value=f'{avg_temp:.1f}',
            delta=f'{delta_temp:+.1f}°C',
            delta_color='normal' if delta_temp >= 0 else 'inverse'
        )
        st.metric(
            label=f'{loc} Avg Humidity (%)',
            value=f'{avg_hum:.1f}',
            delta=f'{delta_hum:+.1f}%',
            delta_color='normal' if delta_hum >= 0 else 'inverse'
        )

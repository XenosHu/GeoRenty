import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Load data
raw = pd.read_csv('zillow.csv')

# Parse the 'price' column to integers
raw['price'] = raw['price'].replace('[\$,\/mo]', '', regex=True).astype(int)

# Calculate the mean latitude and longitude
mean_lat = raw['latitude'].mean()
mean_lon = raw['longitude'].mean()

# Streamlit slider for adjusting the pitch (view angle)
pitch = st.slider('Adjust View Angle', 0, 60, 50)

# PyDeck map
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=mean_lat,
        longitude=mean_lon,
        zoom=11,
        pitch=pitch,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=raw,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
        pdk.Layer(
            'ColumnLayer',
            data=raw,
            get_position='[longitude, latitude]',
            get_elevation='price',
            elevation_scale=1,
            radius=100,
            get_fill_color='[255, 165, 0, 255]',  # Orange color
            pickable=True,
            extruded=True,
        ),
    ],
))

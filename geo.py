import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Load data
raw = pd.read_csv('zillow.csv')

# Remove rows where 'price' is NaN
raw = raw.dropna(subset=['price'])

# Clean the 'price' column to remove non-numeric characters (like '$', ',', '/mo', '+')
raw['price'] = raw['price'].replace('[\$,\/mo\+]', '', regex=True)

# Convert the 'price' column to integers
raw['price'] = raw['price'].astype(int)
raw = raw[raw['homeType']== 'APARTMENT']

# Calculate the mean latitude and longitude
max_lat = raw['latitude'].max()
max_lon = raw['longitude'].max()

# PyDeck map
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=max_lat,
        longitude=max_lon,
        zoom=11
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

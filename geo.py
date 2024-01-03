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

raw['postal_code'] = raw['postal_code'].astype(int)

# Group by 'postal_code' and calculate the average price
grouped_data = raw.groupby('postal_code').agg({'price': 'mean', 'latitude': 'mean', 'longitude': 'mean'}).reset_index()

# Define a function to convert price to a color (green to red gradient)
def price_to_color(price):
    max_price = grouped_data['price'].max()
    min_price = grouped_data['price'].min()
    normalized_price = (price - min_price) / (max_price - min_price)
    red = int(normalized_price * 255)
    green = int((1 - normalized_price) * 255)
    blue = 0
    return [red, green, blue, 255]

grouped_data['color'] = grouped_data['price'].apply(price_to_color)

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
            data=grouped_data,
            get_position='[longitude, latitude]',
            get_elevation='price',
            elevation_scale=1,
            get_fill_color='color',
            radius=100,
            pickable=True,
            extruded=True,
        ),
    ],
))

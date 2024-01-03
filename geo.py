import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import json

# Load data
raw = pd.read_csv('zillow.csv')

# Remove rows where 'price' is NaN
raw = raw.dropna(subset=['price'])

# Clean the 'price' column to remove non-numeric characters (like '$', ',', '/mo', '+')
raw['price'] = raw['price'].replace('[\$,\/mo\+]', '', regex=True)

# Convert the 'price' column to integers
raw['price'] = raw['price'].astype(int)
raw = raw[raw['homeType']== 'APARTMENT']

raw = raw[raw['price'] <= 10000]

# Calculate the mean latitude and longitude
max_lat = raw['latitude'].max()
max_lon = raw['longitude'].max()

raw['postal_code'] = raw['postal_code'].astype(str)

# Group by 'postal_code' and calculate the average price
grouped_data = raw.groupby('postal_code').agg({'price': 'mean', 'latitude': 'mean', 'longitude': 'mean'}).reset_index()


# Get the maximum price for the gradient calculation
max_price = grouped_data['price'].max()

# Define a function to convert price to a gradient color (green to red)
def price_to_color(price):
    normalized_price = price / max_price
    red = int(normalized_price * 255)
    green = int((1 - normalized_price) * 255)
    blue = 0
    return [red, green, blue, 255]

grouped_data['color'] = grouped_data['price'].apply(price_to_color)


# Replace 'path_to_geojson_file' with the actual path or URL to the GeoJSON file
with open('georef-united-states-of-america-zc-point.geojson', 'r') as f:
    geojson_data = json.load(f)

for feature in geojson_data['features']:
    # Extract zip code from feature properties
    zip_code = feature['properties']['ZIP_CODE_FIELD']  # Replace with actual field name
    
    # Find matching data in grouped_data
    match = grouped_data[grouped_data['postal_code'] == zip_code]
    
    if not match.empty:
        # Add average price and color to GeoJSON properties
        feature['properties']['average_price'] = match.iloc[0]['price']
        feature['properties']['color'] = price_to_color(match.iloc[0]['price'])

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=40.703,
        longitude=-74.009,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'GeoJsonLayer',
            data=geojson_data,
            get_fill_color='properties.color',
            get_elevation='properties.average_price',
            elevation_scale=1,
            pickable=True,
            extruded=True,
        ),
    ],
))

# # PyDeck map with GeoJsonLayer
# st.pydeck_chart(pdk.Deck(
#     map_style=None,
#     initial_view_state=pdk.ViewState(
#         latitude=40.703,
#         longitude=-74.009,
#         zoom=11,
#         pitch=50,
#     ),
#     layers=[
#         pdk.Layer(
#             'GeoJsonLayer',
#             data=geojson_data,
#             get_fill_color='color',  # Assuming 'color' is set in the GeoJSON properties
#             get_elevation='price',   # Assuming 'price' is set in the GeoJSON properties
#             elevation_scale=1,
#             pickable=True,
#             extruded=True,
#         ),
#     ],
# ))

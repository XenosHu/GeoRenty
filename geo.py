# import streamlit as st
# import pandas as pd
# import numpy as np
# import pydeck as pdk


# chart_data = pd.DataFrame(
#    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#    columns=['lat', 'lon'])

# st.pydeck_chart(pdk.Deck(
#     map_style=None,
#     initial_view_state=pdk.ViewState(
#         latitude=37.76,
#         longitude=-122.4,
#         zoom=11,
#         pitch=50,
#     ),
#     layers=[
#         pdk.Layer(
#            'HexagonLayer',
#            data=chart_data,
#            get_position='[lon, lat]',
#            radius=200,
#            elevation_scale=4,
#            elevation_range=[0, 1000],
#            pickable=True,
#            extruded=True,
#         ),
#         pdk.Layer(
#             'ScatterplotLayer',
#             data=chart_data,
#             get_position='[lon, lat]',
#             get_color='[200, 30, 0, 160]',
#             get_radius=200,
#         ),
#     ],
# ))



import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap


# Load cleaned data (replace 'cleaned_zillow_data' with the path to your cleaned data file)
cleaned_zillow_data = pd.read_csv('zillow.csv')

# Initialize the map
m = leafmap.Map(center=[cleaned_zillow_data['latitude'].mean(), cleaned_zillow_data['longitude'].mean()], zoom=10)

# Add points to the map
for _, row in cleaned_zillow_data.iterrows():
    m.add_marker(location=[row['latitude'], row['longitude']], 
                 popup=f"Year Built: {row['yearBuilt']}, City: {row['city']}, State: {row['state']}, Bedrooms: {row['bedrooms']}, Bathrooms: {row['bathrooms']}, Area: {row['area']}")

# Display the map
st.title("Zillow Property Map")
st.write("Interactive map of properties")
st.leafmap(m)

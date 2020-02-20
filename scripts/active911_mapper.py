# -*- coding: utf-8 -*-
# This script has been included for historical purposes. It allows the same type of functionality as 911maps, but with static HTML.
"""
Created on Sat Nov 17 14:28:17 2018

@author: Gavin Rozzi
"""

import folium
import branca
import pandas as pd
import numpy as np

active911_calls = pd.read_csv('tr911_cleaned.csv', index_col='id')

latitude = active911_calls.lat.tolist()

longitude = latitude = active911_calls.lon.tolist()

latlong = dict(zip(latitude, longitude))

df = pd.DataFrame.from_dict(latlong, orient='index')

df2 = pd.read_csv('tr911_cleaned.csv', index_col='id')



m = folium.Map(location=[39.991895, -74.191679], zoom_start=12.5)

def iterate_items():
    for item in df2['description']:
        print(item)

for item in df2['description']:
    print(item)



for index, row in active911_calls.iterrows():
    html = """
    <h1> Test </h1><br>
    <h2> Test </h2> 
    With a few lines of code...
    <p>
     part   
    
    </p>
    """
 
    folium.Marker([row['lat'], row['lon']],
                        popup=html,
                       ).add_to(m)

m.save('index.html')


# previous instead of html row['description']
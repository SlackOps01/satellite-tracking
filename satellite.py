import os
from dotenv import load_dotenv
import requests
import json
import plotly.express as px
import pandas as pd
from skyfield.api import EarthSatellite, load
import logging

logging.basicConfig(level=logging.DEBUG, filename="api_logs.txt", filemode='w+')

ts = load.timescale()
t = ts.now()

load_dotenv()

api_key = os.getenv("sat_api_key")
satellites = {
    38014: "NIGCOMSAT 1R",
    37790: "NIGERIASAT X",
    37789: "NIGERIASAT 2",
    31395: "NIGCOMSAT 1",
    27941: "NIGERIASAT 1",
    25544: "ISS"
}

data = pd.DataFrame()
for satellite_id, satellite_name in satellites.items():
    # logging.debug("MAKING REQUEST...")
    url = f"https://api.n2yo.com/rest/v1/satellite/tle/{satellite_id}&apiKey={api_key}"

    html_data = requests.get(url)
    # logging.debug(f"STATUS CODE: {html_data.status_code}")
    html_content = html_data.json()
    tle = str(html_content['tle'])
    tle_split = tle.split("\n")
    line1 = tle_split[0]
    line2 = tle_split[1]

    # print(f"line1: {line1}")
    # print(f"line2: {line2}")

    satellite = EarthSatellite(line1, line2, "ISS", ts)
    geocentric = satellite.at(t)
    subpoint = geocentric.subpoint()

    # Extract Latitude, Longitude, and Altitude
    latitude = subpoint.latitude.degrees
    longitude = subpoint.longitude.degrees
    altitude = subpoint.elevation.km


    # print(f"Latitude: {latitude:.6f}°")
    # print(f"Longitude: {longitude:.6f}°")
    # print(f"Altitude: {altitude:.2f} km")
    # data = pd.DataFrame({
    #     "Longitude": [longitude],
    #     "Latitude": [latitude], 
    #     "Label": ['ISS POS']
    # })
    data = pd.concat(
        [
            data, pd.DataFrame({
                "Longitude": [longitude],
                "Latitude": [latitude],
                "Label": [satellite_name]
            })
        ]
    )

fig = px.scatter_geo(
    data,
    lat='Latitude',
    lon='Longitude',
    text='Label',  # Add labels to points
    title="Satellite Positions",
    projection="natural earth"
)

# Customize the map appearance
fig.update_layout(
    geo=dict(
        showland=True,
        landcolor="rgb(212, 212, 212)",
        showocean=True,
        oceancolor="rgb(204, 230, 255)",
    )
)

fig.show()


# print(json.dumps(html_content, indent=4))
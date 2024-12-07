from fastapi import FastAPI
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import requests
import os
import plotly.express as px 
import plotly.io as pio
from skyfield.api import load, EarthSatellite
import pandas as pd

app = FastAPI()
load_dotenv()
api_key = os.getenv("sat_api_key")
ts = load.timescale()
t = ts.now()

def make_request(sat_id: int):
    url = f"https://api.n2yo.com/rest/v1/satellite/tle/{sat_id}&apiKey={api_key}"
    response = requests.get(url)
    response_json = response.json()
    sat_info = response_json['info']
    
    sat_name = sat_info['satname']
    tle  = str(response_json['tle'])
    tle_split = tle.split("\n")
    line1 = tle_split[0]
    line2 = tle_split[1]
    return {
        "sat_id": sat_id,
        "sat_name": sat_name,
        "tle": tle,
        "line_1": line1,
        "line_2": line2
    }

def parse_tle(line1, line2, sat_name, sat_id):
    satellite = EarthSatellite(line1, line2, sat_name, ts)
    geocentric = satellite.at(t)
    subpoint = geocentric.subpoint()
    
    latitude = subpoint.latitude.degrees
    longitude = subpoint.longitude.degrees
    altitude = subpoint.elevation.km
    
    return {
        "sat_id": sat_id,
        "sat_name": sat_name,
        "longitude": longitude,
        "latitude": latitude,
        "altitude": altitude
    }


@app.get("/")
def home():
    return {
        "message": "Hello World!"
    }

@app.get("/satellite/tle/{sat_id}")
def get_satellite_tle(sat_id: int):
    return make_request(sat_id)

@app.get("/satellite/track/{sat_id}")
def track_satellite(sat_id: int):
    tle_data = make_request(sat_id)
    line1 = tle_data["line_1"]
    line2 = tle_data["line_2"]
    sat_name = tle_data["sat_name"]
    
    return parse_tle(line1, line2, sat_name, sat_id)
    
@app.get("/satellite/visualization/{sat_id}")
def generate_visualization(sat_id: int):
    tle_data = make_request(sat_id)
    line1 = tle_data['line_1']
    line2 = tle_data['line_2']
    label = tle_data['sat_name']
    tle_parsed = parse_tle(line1, line2, label, sat_id)
    data = pd.DataFrame({
        "Longitude": [tle_parsed["longitude"]],
        "Latitude": [tle_parsed['latitude']],
        "Label": [label]
    })
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
    pio.write_html(fig, file='satellites.html', auto_open=False)
    return FileResponse("satellites.html")
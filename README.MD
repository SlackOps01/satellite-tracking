# Satellite Tracker API

This FastAPI application provides an interface to access real-time satellite data and visualize their positions.

## Features

*   Retrieves Two-Line Element (TLE) data for satellites using a provided satellite ID and an API key.
*   Calculates the current position (longitude, latitude, altitude) of a satellite based on its TLE data.
*   Generates a map visualization of the satellite's position on Earth.

## Requirements

*   Python 3.x
*   FastAPI
*   `requests`
*   `python-dotenv`
*   `skyfield`
*   `pandas`
*   `plotly.express`
*   `plotly.io`

## Installation

1.  Create a virtual environment (recommended).

2.  Install required libraries:

    ```bash
    pip install fastapi requests python-dotenv skyfield pandas plotly
    ```

## Configuration

1.  Create a `.env` file in your project directory with the following line:

    ```
    sat_api_key=YOUR_API_KEY
    ```

    Replace `YOUR_API_KEY` with a valid API key from a satellite data provider like n2yo.com.

## Running the Application

1.  Start the server:

    ```bash
    uvicorn main:app --reload
    ```

    (Replace `main` with your main application file name if it's different)

## API Endpoints

| Endpoint                      | Description                                                                     |
| ----------------------------- | ------------------------------------------------------------------------------- |
| `/`                           | Returns a simple "Hello World!" message                                           |
| `/satellite/tle/{sat_id}`      | Retrieves TLE data for a satellite by its ID                                   |
| `/satellite/track/{sat_id}`    | Calculates and returns the current position of a satellite                       |
| `/satellite/visualization/{sat_id}` | Generates and returns an HTML map visualization of the satellite's position |

## Usage

1.  **Retrieving TLE Data:**

    ```bash
    curl http://localhost:8000/satellite/tle/12345  # Replace 12345 with the satellite ID
    ```

    This will return the TLE data for the satellite in JSON format.

2.  **Tracking Satellite:**

    ```bash
    curl http://localhost:8000/satellite/track/12345  # Replace 12345 with the satellite ID
    ```

    This will return the current position (longitude, latitude, altitude) of the satellite in JSON format.

3.  **Generating Visualization:**

    ```bash
    curl http://localhost:8000/satellite/visualization/12345  # Replace 12345 with the satellite ID
    ```

    This will download an HTML file named `satellites.html` containing a map visualization of the satellite's position. You can open this file in a web browser to view the map.

## Note

*   This application retrieves TLE data from an external API. You may need to create an account and obtain an API key from the chosen provider.
*   The accuracy of the satellite position is based on the TLE data, which can be updated periodically.
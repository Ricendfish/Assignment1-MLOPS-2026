# Automated Weather Pipeline with GitHub Pages

This project implements an automated data pipeline that collects weather forecasts for three cities, stores the data in a SQL database, generates a poem using an LLM, and publishes the result using GitHub Pages.

The pipeline runs automatically using GitHub Actions.

## Cities Used

- Rajshahi (Place of Birth)
- Dhaka (Last residence before Aalborg)
- Aalborg (Current city)

## Weather Variables

The pipeline retrieves the following weather variables from the Open-Meteo API:

- Temperature
- Precipitation
- Wind Speed

## Pipeline Overview

The pipeline performs the following steps:

1. Fetch weather forecast data from the Open-Meteo API.
2. Extract weather variables for the three cities.
3. Store the data in a SQLite database (`weather.db`).
4. Send the weather information to the Groq API to generate a poem.
5. Generate an HTML page displaying the poem.
6. Publish the page automatically via GitHub Pages.


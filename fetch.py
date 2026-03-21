import requests
import sqlite3
import os
from groq import Groq

# Cities and coordinates
locations = {
    "Rajshahi": (24.3745, 88.6042),
    "Dhaka": (23.8103, 90.4125),
    "Aalborg": (57.0488, 9.9217)
}

API_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_weather(city, lat, lon):

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "temperature_2m",
            "precipitation",
            "wind_speed_10m"
        ],
        "forecast_days": 1,
        "timezone": "auto"
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    if "hourly" not in data:
        print(data)
        raise Exception("Weather API returned unexpected data")

    temp = data["hourly"]["temperature_2m"][0]
    rain = data["hourly"]["precipitation"][0]
    wind = data["hourly"]["wind_speed_10m"][0]

    return temp, rain, wind


def save_to_db(city, temp, rain, wind):

    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            city TEXT,
            temperature REAL,
            precipitation REAL,
            wind REAL
        )
    """)

    cursor.execute(
        "INSERT INTO weather VALUES (?, ?, ?, ?)",
        (city, temp, rain, wind)
    )

    conn.commit()
    conn.close()


def generate_poem(weather_text):

    # Get API key from GitHub Secrets
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise Exception("GROQ_API_KEY not found in environment variables")

    client = Groq(api_key=api_key)

    prompt = f"""
Compare tomorrow's weather in the following cities:

{weather_text}

Write a short poetic comparison describing temperature, rain, and wind.
Suggest which city would be the nicest place tomorrow.

Write the poem in two languages:
1. English
2. Bengali
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    poem = completion.choices[0].message.content
    return poem


def create_html(poem, weather_text):

    html = f"""
<html>
<head>
<title>Weather Comparison</title>
</head>

<body>

<h1>Weather Comparison: Rajshahi vs Dhaka vs Aalborg</h1>

<h2>Forecast Data</h2>
<pre>
{weather_text}
</pre>

<h2>Generated Poem</h2>
<pre>
{poem}
</pre>

</body>
</html>
"""

    with open("docs/index.html", "w") as f:
        f.write(html)


def main():

    weather_text = ""

    for city, coords in locations.items():

        temp, rain, wind = fetch_weather(city, coords[0], coords[1])

        save_to_db(city, temp, rain, wind)

        weather_text += f"{city}: Temp {temp}°C, Rain {rain}mm, Wind {wind} km/h\n"

    poem = generate_poem(weather_text)

    create_html(poem, weather_text)


if __name__ == "__main__":
    main()

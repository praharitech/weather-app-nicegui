import os

import requests
from dotenv import load_dotenv
from nicegui import run, ui

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("API_KEY")


# Function to fetch weather data from OpenWeatherMap API
async def fetch_weather_data(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = await run.io_bound(requests.get, url)
    print(response.status_code)

    if response.status_code == 200:
        data = response.json()
        print(data)
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return temperature, humidity, wind_speed
    else:
        return None, None, None


# Function to display weather data in the UI
async def fetch_weather(location, labels):
    temperature, humidity, wind_speed = await fetch_weather_data(location)
    if temperature is not None:
        labels["temperature"].set_text(f"Temperature: {temperature}°C")
        labels["humidity"].set_text(f"Humidity: {humidity}%")
        labels["wind_speed"].set_text(f"Wind Speed: {wind_speed} m/s")
    else:
        ui.notify(f"Could not fetch data for {location}", color="red")


# Page Layout
def create_layout():
    labels = {}
    with ui.column().classes("w-full items-center"):
        ui.label("Weather App").classes("text-4xl font-bold mb-4").style(
            "color: #3498db;"
        )
        with ui.row().classes("w-full justify-center items-center"):
            ui.label("Enter Location:").classes("mr-2")
            location_input = ui.input(placeholder="City Name").props("clearable")
            ui.button(
                "Get Weather",
                on_click=lambda: fetch_weather(location_input.value, labels),
            ).classes("primary rounded-full")

        # Placeholder for weather info
        with ui.column().classes("w-full items-center mt-8"):
            labels["temperature"] = ui.label("Temperature: --°C").classes("text-xl")
            labels["humidity"] = ui.label("Humidity: --%").classes("text-xl")
            labels["wind_speed"] = ui.label("Wind Speed: -- m/s").classes("text-xl")


# Initialize Layout
create_layout()

ui.run()

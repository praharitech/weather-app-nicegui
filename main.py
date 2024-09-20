import os

import requests
from dotenv import load_dotenv
from nicegui import app, ui

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("API_KEY")


# Function to fetch weather data from OpenWeatherMap API
def fetch_weather_data(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return temperature, humidity, wind_speed
    else:
        return None, None, None


# Page builder function for the weather app
@ui.page("/")
def main_page():
    # Function to display weather data in the UI
    def fetch_weather(location):
        temperature, humidity, wind_speed = fetch_weather_data(location)
        if temperature is not None:
            temperature_label.set_text(f"Temperature: {temperature}°C")
            humidity_label.set_text(f"Humidity: {humidity}%")
            wind_speed_label.set_text(f"Wind Speed: {wind_speed} m/s")
        else:
            ui.notify(f"Could not fetch data for {location}", color="red")

    # Function to save the location in app.storage.user
    def save_location(location):
        locations = app.storage.user.get("locations", [])
        if location not in locations and len(locations) < 5:
            locations.append(location)
            app.storage.user["locations"] = locations
            ui.notify(f"Location '{location}' saved!", color="green")
        else:
            ui.notify("Location already saved or max limit reached", color="red")

    # Function to get saved locations
    def get_saved_locations():
        return app.storage.user.get("locations", [])

    # Function to display saved locations in the UI
    def show_saved_locations():
        saved_locations = get_saved_locations()
        with ui.column().classes("w-full items-center mt-8"):
            ui.label("Saved Locations").classes("text-xl font-bold")
            for loc in saved_locations:
                ui.button(loc, on_click=lambda loc=loc: fetch_weather(loc)).classes(
                    "secondary rounded"
                )

    # Create the main UI layout
    with ui.column().classes("w-full items-center"):
        ui.label("Weather App").classes("text-4xl font-bold mb-4")
        with ui.row().classes("w-full justify-center items-center"):
            ui.label("Enter Location:").classes("mr-2")
            location_input = ui.input(placeholder="City Name").props("clearable")
            ui.button(
                "Get Weather", on_click=lambda: fetch_weather(location_input.value)
            ).classes("primary rounded")
            ui.button(
                "Save Location", on_click=lambda: save_location(location_input.value)
            ).classes("secondary rounded")

        # Placeholders for weather data
        global temperature_label, humidity_label, wind_speed_label
        temperature_label = ui.label("Temperature: --°C").classes("text-xl")
        humidity_label = ui.label("Humidity: --%").classes("text-xl")
        wind_speed_label = ui.label("Wind Speed: -- m/s").classes("text-xl")

    # Display saved locations
    show_saved_locations()


# Start the app
ui.run(storage_secret="averyveryverylognsecretstring")

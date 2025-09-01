import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv('WEATHER_API_KEY')
if not API_KEY:
    raise ValueError("Weather API key is not set in the .env file")

BASE_URL = "http://api.weatherapi.com/v1/"

CITIES = [
    {"name": "Kano"},
    {"name": "Kaduna"},
    {"name": "Lagos"},
    {"name": "Abuja"},
    {"name": "Calabar"}
]

def fetch_weather_data():
    weather_data = []
    
    for city in CITIES:
        params = {
            'key': API_KEY,
            'q': f"{city['name']}",
            'aqi': 'no',
        }
        
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            weather_data.append({
                "city_name": data["location"]["name"],
                "country": data["location"]["country"],
                "latitude": data["location"]["lat"],
                "longitude": data["location"]["lon"],
                "temperature": data["current"]["temp_c"],
                "humidity": data["current"]["humidity"],
                "pressure": data["current"]["pressure_mb"],
                "wind_speed": data["current"]["wind_kph"],
                "datetime": data["location"]["localtime"].replace(" ", "T")
            })
        else:
            print(f"Error fetching data for {city['name']}: {response.status_code}")
    
    return weather_data

if __name__ == "__main__":
    data = fetch_weather_data()
    for item in data:
        print(item)

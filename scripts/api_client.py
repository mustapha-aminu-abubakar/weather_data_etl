import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

API_KEY = os.getenv('WEATHER_API_KEY')
if not API_KEY:
    raise ValueError("Weather API key is not set in the .env file")

BASE_URL = "http://api.weatherapi.com/v1/current.json"

CITIES = [
    "Abakaliki",   # Ebonyi
    "Abeokuta",    # Ogun
    "Ado-Ekiti",   # Ekiti
    "Akure",       # Ondo
    "Asaba",       # Delta
    "Awka",        # Anambra
    # "Bauchi",      # Bauchi
    # "Benin City",  # Edo
    # "Birnin Kebbi",# Kebbi
    # "Calabar",     # Cross River
    # "Damaturu",    # Yobe
    # "Dutse",       # Jigawa
    # "Enugu",       # Enugu
    # "Gombe",       # Gombe
    # "Gusau",       # Zamfara
    # "Ibadan",      # Oyo
    # "Ilorin",      # Kwara
    # "Jalingo",     # Taraba
    # "Jos",         # Plateau
    # "Kaduna",      # Kaduna
    # "Kano",        # Kano
    # "Katsina",     # Katsina
    # "Lafia",       # Nasarawa
    # "Lokoja",      # Kogi
    # "Maiduguri",   # Borno
    # "Makurdi",     # Benue
    # "Minna",       # Niger
    # "Osogbo",      # Osun
    # "Owerri",      # Imo
    # "Port Harcourt", # Rivers
    # "Sokoto",      # Sokoto
    # "Umuahia",     # Abia
    # "Uyo",         # Akwa Ibom
    # "Yenagoa",     # Bayelsa
    # "Yola",        # Adamawa
    # "Zaria",       # (Kaduna has Kaduna City, not Zaria)
    # "Abuja"        # Federal Capital Territory
]


def fetch_weather_data():
    weather_data = []
    
    for i, city in enumerate(CITIES, start=1):
        params = {
            'key': API_KEY,
            'q': city,
            'aqi': 'no',
        }
        
        try:
            response = requests.get(BASE_URL, params=params)
            
            if response.status_code == 200:
                data = response.json()
                weather_data.append({
                    "city_id": i,
                    "city_name": data["location"]["name"],
                    "country": data["location"]["country"],
                    "latitude": data["location"]["lat"],
                    "longitude": data["location"]["lon"],
                    "temperature": data["current"]["temp_c"],
                    "humidity": data["current"]["humidity"],
                    "pressure": data["current"]["pressure_mb"],
                    "wind_speed": data["current"]["wind_kph"],
                    "date": data["location"]["localtime"].split(" ")[0],
                    "time": data["location"]["localtime"].split(" ")[1],
                })
        except Exception as e:
            print(f"Error fetching data for {city}: {response.status_code}, {e}")
        time.sleep(500)
    
    return weather_data

if __name__ == "__main__":
    data = fetch_weather_data()
    for item in data:
        print(item)

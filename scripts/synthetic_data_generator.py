import random
from datetime import datetime, timedelta
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_HOST = os.getenv('MYSQL_HOST')
DB_PORT = os.getenv('MYSQL_PORT')
DB_NAME = os.getenv('MYSQL_DB')

cities = [
    "Abakaliki",   # Ebonyi
    "Abeokuta",    # Ogun
    "Ado-Ekiti",   # Ekiti
    "Akure",       # Ondo
    "Asaba",       # Delta
    "Awka",        # Anambra
    "Bauchi",      # Bauchi
    "Benin City",  # Edo
    "Birnin Kebbi",# Kebbi
    "Calabar",     # Cross River
    "Damaturu",    # Yobe
    "Dutse",       # Jigawa
    "Enugu",       # Enugu
    "Gombe",       # Gombe
    "Gusau",       # Zamfara
    "Ibadan",      # Oyo
    "Ilorin",      # Kwara
    "Jalingo",     # Taraba
    "Jos",         # Plateau
    "Kaduna",      # Kaduna
    "Kano",        # Kano
    "Katsina",     # Katsina
    "Lafia",       # Nasarawa
    "Lokoja",      # Kogi
    "Maiduguri",   # Borno
    "Makurdi",     # Benue
    "Minna",       # Niger
    "Osogbo",      # Osun
    "Owerri",      # Imo
    "Port Harcourt", # Rivers
    "Sokoto",      # Sokoto
    "Umuahia",     # Abia
    "Uyo",         # Akwa Ibom
    "Yenagoa",     # Bayelsa
    "Yola",        # Adamawa
    "Zaria",       # (Kaduna has Kaduna City, not Zaria)
    "Abuja"        # Federal Capital Territory
]

def generate_cities():
    """
    Generate n synthetic cities and insert into the cities table.
    """
    conn = mysql.connector.connect(
        user= DB_USER,
        password= DB_PASSWORD,
        database= DB_NAME,
        port= DB_PORT,
        host = DB_HOST
    )
    cursor = conn.cursor()
    country = 'Nigeria'
    
    cities_data=[]
    for i, city in enumerate(cities, start=1):
        city_name = city
        country = country
        latitude = round(random.uniform(-90, 90), 4)
        longitude = round(random.uniform(-180, 180), 4)
        city_id = i
        cities_data.append((city_id, city_name, country, latitude, longitude))
        # print(cities_data)
    cursor.executemany(
        "INSERT INTO cities (city_id, city_name, country, latitude, longitude) VALUES (%s, %s, %s, %s, %s)",
        cities_data
    )
    conn.commit()
    cursor.close()
    conn.close()
    return cities_data

def generate_weather_measurements(n=20, start_time=None):
    """
    Generate n synthetic weather measurements for a given city_id in 5 minute intervals.
    """
    conn = mysql.connector.connect(
        user= DB_USER,
        password= DB_PASSWORD,
        database= DB_NAME,
        port= DB_PORT,
        host = DB_HOST
    )    
    cursor = conn.cursor()
    if start_time is None:
        start_time = datetime.now().replace(second=0, microsecond=0)
    measurements = []
    for i in range(n):
        dt = start_time + timedelta(minutes=5*i)
        for j, city in enumerate(cities, start=1):
            temperature = round(random.uniform(20, 35), 2)
            humidity = round(random.uniform(40, 90), 2)
            pressure = random.randint(950, 1050)
            wind_speed = round(random.uniform(0, 15), 2)
            measurements.append((j, temperature, humidity, dt.date(), dt.time(), pressure, wind_speed))
    cursor.executemany(
        "INSERT INTO weather_measurements (city_id, temperature, humidity, date, time, pressure, wind_speed) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        measurements
    )
    conn.commit()
    cursor.close()
    conn.close()
    return measurements

if __name__ == "__main__":
    generate_cities()
    generate_weather_measurements(20)
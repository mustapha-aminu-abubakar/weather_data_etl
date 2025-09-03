from flask import Flask, jsonify, render_template
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import os
import mysql.connector

load_dotenv()

app = Flask(__name__)

DB_USER = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_HOST = os.getenv('MYSQL_HOST')
DB_PORT = os.getenv('MYSQL_PORT')
DB_NAME = os.getenv('MYSQL_DB')

DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(DATABASE_URL)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather_data')
def get_weather_data():
    with mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT) as connection:
        
        cursor = connection.cursor()
        cursor.execute("""
        SELECT c.city_name, w.date, w.time, w.temperature, w.humidity
        FROM weather_measurements w
        JOIN cities c ON w.city_id = c.city_id
        ORDER BY c.city_name, w.date
        """)
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns=[i[0] for i in cursor.description])
    df['time'] = df['time'].apply(lambda t: str(t) if isinstance(t, str) else (datetime.min + t).time().strftime('%H:%M:%S'))
    df['datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'])
    print(df['datetime'][:5])  
    df['temperature'] = df['temperature'].astype(float)
    df['humidity'] = df['humidity'].astype(float)
    
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)

from pyspark.sql.functions import col, to_date, to_timestamp, round, dense_rank
from pyspark.sql.window import Window

def transform_weather_data(spark, raw_json):    
    # Convert to DataFrame
    df = spark.createDataFrame(raw_json)
    
    fact_columns = ['date', 'time', 'city_id', 'temperature', 'humidity', 'pressure', 'wind_speed']
    fact_df = df.select(fact_columns)
    
    dim_columns = ['city_id', 'city_name', 'country', 'latitude', 'longitude']
    dim_df = df.select(dim_columns).dropDuplicates()
    print('---------------data transformer worked-------------------------')
    
    return fact_df, dim_df

if __name__ == "__main__":
    from pyspark.sql import SparkSession
    
    spark = SparkSession.builder \
        .appName("WeatherDataTransformer") \
        .getOrCreate()

    test_data = [
        {
            'city_id': 1,
            'city_name': 'New York',
            'country': 'US',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'temperature': 22.5,
            'humidity': 60,
            'pressure': 1015,
            'wind_speed': 5.1,
            'date': '2023-05-01',
            'time': '12:00:00'
        },
        {
            'city_id': 2,
            'city_name': 'London',
            'country': 'GB',
            'latitude': 51.5074,
            'longitude': -0.1278,
            'temperature': 15.3,
            'humidity': 72,
            'pressure': 1008,
            'wind_speed': 4.2,
            'date': '2023-05-01',
            'time': '12:00:00'
        }
    ]

    fact_df, dim_df = transform_weather_data(spark, test_data)
    
    print("Fact DataFrame:")
    fact_df.show()
    
    print("\nDimension DataFrame:")
    dim_df.show()

    spark.stop()

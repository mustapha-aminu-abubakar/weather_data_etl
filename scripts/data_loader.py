import os
import sys
from pyspark.sql import SparkSession
from dotenv import load_dotenv
import logging
import mysql.connector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

load_dotenv(os.path.join(project_root, '.env'))

DB_USER = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_HOST = os.getenv('MYSQL_HOST')
DB_PORT = os.getenv('MYSQL_PORT')
DB_NAME = os.getenv('MYSQL_DB')

JDBC_URL = f"jdbc:mysql://{DB_HOST}:{DB_PORT}/{DB_NAME}?useSSL=false&serverTimezone=UTC"

def create_database():
    try:
        # Connect without selecting a database
        with mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        ) as connection:
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            logger.info(f"Database `{DB_NAME}` created successfully (or already exists).")

    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        raise


def create_tables():
    # engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    try:
        with mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME) as connection:
            cursor = connection.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cities (
                    city_id INT PRIMARY KEY,
                    city_name VARCHAR(255),
                    country VARCHAR(20),
                    latitude FLOAT,
                    longitude FLOAT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_measurements (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    city VARCHAR(100) NOT NULL,
                    city_id INT NOT NULL
                    temperature FLOAT NOT NULL,
                    humidity FLOAT NOT NULL,
                    date DATE NOT NULL,
                    time TIME NOT NULL,
                    pressure INT NOT NULL,
                    wind_speed FLOAT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        logger.info("Tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        raise

def load_data(spark, fact_df, dim_df):
    logger.info("Starting data load process")

    try:
        # ----------------------------
        # Load dimension table (cities)
        # ----------------------------
        dim_df.write \
            .format("jdbc") \
            .option("url", JDBC_URL) \
            .option("dbtable", "cities") \
            .option("user", DB_USER) \
            .option("password", DB_PASSWORD) \
            .mode("overwrite") \
            .save()

        logger.info("Cities data loaded successfully")

        # ----------------------------
        # Load fact table (weather_measurements)
        # ----------------------------
        fact_df.write \
            .format("jdbc") \
            .option("url", JDBC_URL) \
            .option("dbtable", "weather_measurements") \
            .option("user", DB_USER) \
            .option("password", DB_PASSWORD) \
            .mode("append") \
            .save()

        logger.info("Weather measurements data loaded successfully")

    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

    logger.info("Data loading process completed")


if __name__ == "__main__":
    create_database()
    create_tables()

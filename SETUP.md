# 📘 Setup Guide for Weather Data Integration

This guide explains how to set up and run the project in GitHub Codespaces.

## 1. Open in Codespaces

Go to the repo: weather-data-integration

Click Code → Codespaces → New Codespace on main

## 2. Create Virtual Environment

Inside Codespaces terminal:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Install & Configure MySQL
### 4.1 Install MySQL
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install mysql-server mysql-client -y
```

### 4.2 Start MySQL Service
```bash
sudo service mysql start
```

### 4.3 Secure MySQL (optional for dev)
```bash
sudo mysql_secure_installation
```

### 4.4 Create Database and User

Enter the MySQL shell:
```bash
sudo mysql -u root
```

Then run:
```sql
CREATE USER 'newuser'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON *.* TO 'newuser'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

## 5. Initialize Airflow Database
```bash
airflow db init
```

## 6. Create Airflow Admin User
```bash
airflow users create \
    --username admin \
    --password admin \
    --firstname First \
    --lastname Last \
    --role Admin \
    --email admin@example.com
```

## 7. Start Airflow Services

Open two terminals in the workspace.

### Terminal 1 – Scheduler
```bash
airflow scheduler
```

### Terminal 2 – Webserver
```bash
airflow webserver -p 8080
```

## 8. Run Flask App
```bash
flask run --host=0.0.0.0 --port=5000
```

✅ Now Airflow runs the DAGs, MySQL stores the weather data, and Flask serves it on the web.
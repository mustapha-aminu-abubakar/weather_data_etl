# 📘 Setup Guide for Weather Data Integration

This guide explains how to set up and run the project in GitHub Codespaces.

## 1. Open in Codespaces

Go to the repo: weather-data-integration

Click Code → Codespaces → New Codespace on main

## 2. Install Java and Setup Env Variables
Install Java 11
```bash
sudo apt update
sudo apt install openjdk-11-jdk
java -version
```
Setup variables
```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
source ~/.bashrc
```

## 3. Create Virtual Environment

Inside Codespaces terminal:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## 5. Install & Configure MySQL
### 5.1 Install MySQL
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install mysql-server mysql-client -y
```

### 5.2 Start MySQL Service
```bash
sudo service mysql start
```

### 5.3 Secure MySQL (optional for dev)
```bash
sudo mysql_secure_installation
```

### 5.4 Create Database and User

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

## 6. Initialize Airflow Database
```bash
airflow db init
```

## 7. Create Airflow Admin User
```bash
airflow users create \
    --username admin \
    --password admin \
    --firstname First \
    --lastname Last \
    --role Admin \
    --email admin@example.com
```

## 8. Start Airflow Services

Open two terminals in the workspace.

### Terminal 1 – Scheduler
```bash
airflow scheduler
```

### Terminal 2 – Webserver
```bash
airflow webserver -p 8080
```

## 9. Run Flask App
```bash
flask run --host=0.0.0.0 --port=5000
```

✅ Now Airflow runs the DAGs, MySQL stores the weather data, and Flask serves it on the web.
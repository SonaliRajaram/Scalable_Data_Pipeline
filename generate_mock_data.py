import csv, random
from datetime import datetime, timedelta

# 1. Generate research_data.csv
csv_path = "data/research_data.csv"
headers = ["record_id", "timestamp", "experiment_id", "sensor_type", "value", "unit", "status", "lab_id"]
statuses = ["ok", "ok", "ok", "warning", "critical"]

with open(csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    for i in range(1, 101): # Generating 100 rows
        writer.writerow([
            f"REC{i:03d}", 
            (datetime.utcnow() - timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S'),
            f"EXP{random.randint(1,5)}", 
            random.choice(["TEMP", "PRESSURE", "HUMIDITY"]),
            round(random.uniform(10.0, 100.0), 3), 
            "C", 
            random.choice(statuses), 
            f"LAB_{random.choice(['A','B','C','D'])}"
        ])

# 2. Generate system.log
log_path = "data/system.log"
levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
services = ["data-collector", "auth-service", "api-gateway"]

with open(log_path, mode='w') as file:
    for i in range(50):
        timestamp = (datetime.utcnow() - timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S')
        level = random.choice(levels)
        service = random.choice(services)
        file.write(f"{timestamp} [{level}] {service}: Processing event batch {i}\n")

print("Datasets generated successfully in the /data folder!")
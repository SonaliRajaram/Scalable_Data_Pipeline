import pandas as pd, json
from datetime import datetime

# These paths must use the Docker container's internal folder structure, 
CSV_PATH = "/opt/airflow/data/research_data.csv"
OUTPUT = "/opt/airflow/data/processed_csv.json"

def ingest_csv():
    df = pd.read_csv(CSV_PATH)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['ingest_time'] = datetime.utcnow().isoformat()
    
    status_map = {"ok":"OK","warning":"WARNING","critical":"CRITICAL"}
    df['status'] = df['status'].str.lower().map(status_map).fillna("UNKNOWN")
    
    df['is_anomaly'] = df['status'].isin(["WARNING","CRITICAL"])
    df['value'] = df['value'].round(3)
    
    records = df.to_dict(orient="records")
    for r in records:
        r['timestamp'] = str(r['timestamp'])
        
    with open(OUTPUT, "w") as f:
        json.dump(records, f, indent=2)
        
    print(f"[CSV ETL] {len(records)} records written")

# Added execution block for safety
if __name__ == "__main__":
    ingest_csv()
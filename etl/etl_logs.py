import re, json
from datetime import datetime

LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"\[(?P<level>\w+)\]\s+(?P<service>[^:]+):\s+(?P<message>.+)"
)

def ingest_logs():
    records = []
    
    with open("/opt/airflow/data/system.log") as f:
        for line in f:
            m = LOG_PATTERN.match(line.strip())
            if m:
                # m.groupdict() maps the named regex groups into a clean dictionary
                rec = m.groupdict()
                rec['is_error'] = rec['level'] in ("ERROR", "CRITICAL")
                rec['ingest_time'] = datetime.utcnow().isoformat()
                records.append(rec)
                
    with open("/opt/airflow/data/processed_logs.json", "w") as f:
        json.dump(records, f, indent=2)
        
    print(f"[LOGS ETL] {len(records)} log records processed and written.")

# Added execution block for safety
if __name__ == "__main__":
    ingest_logs()
import json, requests

ES_HOST = "http://elasticsearch:9200"

def bulk_index(index, records):
    if not records:
        return
    bulk_body = ""
    for rec in records:
        action = json.dumps({"index": {"_index": index}})
        doc = json.dumps(rec)
        bulk_body += action + "\n" + doc + "\n"
    
    resp = requests.post(
        f"{ES_HOST}/_bulk",
        data=bulk_body,
        headers={"Content-Type": "application/x-ndjson"},
        timeout=30
    )
    result = resp.json()
    print(f"Indexed {len(records)} docs into {index}, errors: {result.get('errors', False)}")

def load_all():
    # Maps the JSON files to their specific Elasticsearch indices
    files_to_indices = {
        "/opt/airflow/data/processed_csv.json": "research_csv",
        "/opt/airflow/data/processed_logs.json": "system_logs",
        "/opt/airflow/data/processed_api.json": "spotify_tracks"
    }
    
    for file_path, index_name in files_to_indices.items():
        try:
            with open(file_path, "r") as f:
                records = json.load(f)
                bulk_index(index_name, records)
        except Exception as e:
            print(f"Failed to load {file_path} into index {index_name}: {e}")

if __name__ == "__main__":
    load_all()
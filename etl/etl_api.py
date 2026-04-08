import os, requests, json
from datetime import datetime

# Output path tailored for the Airflow Docker container
OUTPUT_PATH = "/opt/airflow/data/processed_api.json"

def get_spotify_token():
    cid = os.getenv("SPOTIFY_CLIENT_ID")
    secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if not cid or not secret: 
        return None
        
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(cid, secret), 
        timeout=10
    )
    # Check if the request was successful before trying to get the token
    if r.status_code == 200:
        return r.json().get("access_token")
    return None

def fetch_audio_features(token, track_ids):
    h = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        f"https://api.spotify.com/v1/audio-features?ids={','.join(track_ids)}",
        headers=h, 
        timeout=10
    )
    return r.json().get("audio_features", [])

def ingest_api():
    token = get_spotify_token()
    records = []
    
    if token:
        # 1. Fetch top 20 tracks from a standard Global Top 50 playlist
        h = {"Authorization": f"Bearer {token}"}
        playlist_id = "37i9dQZEVXbMDoHDwVN2tF" # Standard Spotify Global Top 50 ID
        r = requests.get(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=20", 
            headers=h, 
            timeout=10
        )
        items = r.json().get("items", [])
        
        track_data = {}
        track_ids = []
        
        # 2. Extract basic track info
        for item in items:
            track = item.get("track")
            if track:
                tid = track["id"]
                track_ids.append(tid)
                track_data[tid] = {
                    "track_id": tid,
                    "track_name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "popularity": track["popularity"]
                }
        
        # 3. Fetch audio features for those specific tracks
        features = fetch_audio_features(token, track_ids)
        
        # 4. Merge the data together
        for f in features:
            if f:
                tid = f["id"]
                rec = track_data[tid]
                rec.update({
                    "danceability": f["danceability"],
                    "energy": f["energy"],
                    "valence": f["valence"],
                    "tempo": f["tempo"],
                    "ingest_time": datetime.utcnow().isoformat()
                })
                records.append(rec)
        print(f"[API ETL] Successfully fetched {len(records)} live records from Spotify.")
        
    else:
        # 5. SYNTHETIC FALLBACK: Triggered if no credentials are found in the environment
        print("[API ETL] Spotify credentials not found. Generating synthetic dataset.")
        records = [
            {"track_id": "SYN01", "track_name": "Data Drift", "artist": "The Engineers", "danceability": 0.85, "energy": 0.92, "valence": 0.76, "tempo": 125.5, "popularity": 88, "ingest_time": datetime.utcnow().isoformat()},
            {"track_id": "SYN02", "track_name": "Cluster Node", "artist": "DJ Kube", "danceability": 0.65, "energy": 0.81, "valence": 0.45, "tempo": 140.0, "popularity": 72, "ingest_time": datetime.utcnow().isoformat()},
            {"track_id": "SYN03", "track_name": "DAG Dependency", "artist": "Airflow Anthem", "danceability": 0.45, "energy": 0.55, "valence": 0.30, "tempo": 95.0, "popularity": 65, "ingest_time": datetime.utcnow().isoformat()},
            {"track_id": "SYN04", "track_name": "Elastic Search", "artist": "The Indices", "danceability": 0.78, "energy": 0.88, "valence": 0.60, "tempo": 130.0, "popularity": 91, "ingest_time": datetime.utcnow().isoformat()},
            {"track_id": "SYN05", "track_name": "Kafka Stream", "artist": "Realtime", "danceability": 0.90, "energy": 0.95, "valence": 0.85, "tempo": 150.0, "popularity": 95, "ingest_time": datetime.utcnow().isoformat()},
            {"track_id": "SYN06", "track_name": "Pandas Frame", "artist": "The Analysts", "danceability": 0.50, "energy": 0.40, "valence": 0.20, "tempo": 80.0, "popularity": 55, "ingest_time": datetime.utcnow().isoformat()},
            {"track_id": "SYN07", "track_name": "Docker Swarm", "artist": "Container Crew", "danceability": 0.72, "energy": 0.75, "valence": 0.55, "tempo": 115.0, "popularity": 80, "ingest_time": datetime.utcnow().isoformat()},
            {"track_id": "SYN08", "track_name": "Null Exception", "artist": "The Debuggers", "danceability": 0.30, "energy": 0.99, "valence": 0.10, "tempo": 180.0, "popularity": 40, "ingest_time": datetime.utcnow().isoformat()}
        ]

    # 6. Save the data
    with open(OUTPUT_PATH, "w") as f:
        json.dump(records, f, indent=2)

# In the pipeline, Airflow will import and call ingest_api()
if __name__ == "__main__":
    ingest_api()
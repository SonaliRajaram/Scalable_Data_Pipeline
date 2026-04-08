# Scalable Data Engineering Pipeline

Scalable Data Engineering Pipeline is an intelligent data processing system designed to handle multiple data sources (CSV, Logs, APIs) with automated ETL transformations, quality validation, and real-time indexing into Elasticsearch for analytics.

## Features
- **Multi-Source Data Ingestion** – Process CSV files, system logs, and REST API data simultaneously.
- **Automated Data Transformation** – Normalize, enrich, and validate data with custom business logic.
- **Quality Assurance Gates** – Prevent corrupt or incomplete data from reaching production.
- **Scheduled Orchestration** – Apache Airflow manages workflow execution with automatic retries.
- **Container-Based Deployment** – Docker Compose for easy setup and scalability.
- **Real-Time Analytics** – Elasticsearch integration for instant data querying and visualization.

## Project Structure
```
Data_Pipeline/
├── dags/
│   └── research_pipeline_dag.py      # Airflow DAG orchestration workflow
├── etl/
│   ├── etl_csv.py                    # CSV data ingestion and transformation
│   ├── etl_logs.py                   # Log file parsing and processing
│   ├── etl_api.py                    # REST API data fetching and transformation
│   ├── es_loader.py                  # Elasticsearch bulk indexing
│   └── quality_check.py              # Data quality validation gate
├── docker/
│   └── docker-compose.yml            # Docker container orchestration
├── data/
│   ├── research_data.csv             # Sample input data
│   ├── system.log                    # Sample log data
│   ├── processed_csv.json            # Processed CSV output
│   ├── processed_logs.json           # Processed logs output
│   └── processed_api.json            # Processed API data output
├── generate_mock_data.py             # Mock data generator for testing
├── requirements.txt                  # Python dependencies
├── .env                              # Environment configuration
└── README.md                         # Documentation
```

## Prerequisites
- Docker Desktop or Docker Engine (v20.10+)
- Python 3.8 or higher
- 8 GB RAM minimum
- 20 GB free disk space

## Installation & Setup

### 1. Clone the repository
```sh
git clone <repository-url>
cd Data_Pipeline
```

### 2. Create environment configuration
Create a .env file in the root directory with the following variables:
```env
AIRFLOW_HOME=/opt/airflow
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
ELASTICSEARCH_HOST=elasticsearch
ELASTICSEARCH_PORT=9200
```

### 3. Install Python dependencies (Optional - for local development)
```sh
python -m venv venv

On macOS/Linux:
source venv/bin/activate

On Windows:
venv\Scripts\activate

pip install -r requirements.txt
```

### 4. Generate mock data
```sh
python generate_mock_data.py
```
This creates sample datasets in the data directory for testing.

### 5. Start Docker services
```sh
cd docker
docker-compose up -d
```

Wait 30-60 seconds for all services to initialize:
```sh
docker-compose ps
```

### 6. Access the services
- **Airflow Web UI:** http://localhost:8081
  - Username: `admin`
  - Password: `admin`
- **Elasticsearch:** http://localhost:9200
- **PostgreSQL:** localhost:5432

## Usage

### Running the Pipeline Manually
```sh
# Via Airflow UI - Navigate to research_analytics_pipeline and click Play (►)
# Via CLI
cd docker
docker-compose exec airflow-webserver airflow dags trigger research_analytics_pipeline
```

### Monitoring Pipeline Execution
```sh
# View Airflow logs
docker-compose logs -f airflow-webserver

# Check Elasticsearch indices
curl http://localhost:9200/_cat/indices

# Query indexed data
curl -X GET "http://localhost:9200/research_csv/_search?pretty"
```

### Stopping the Pipeline
```sh
cd docker
docker-compose down
```

## Testing

### Run unit tests for ETL modules
```sh
python -m pytest test_main.py -v
```

### Test individual ETL scripts
```sh
python etl/etl_csv.py
python etl/etl_logs.py
python etl/quality_check.py
```

### Validate Docker setup
```sh
docker-compose ps
docker-compose logs [service-name]
```

## Data Flow

```
Data Sources (CSV, Logs, APIs)
        ↓
Apache Airflow Orchestration
        ↓
ETL Transformation Tasks (Parallel)
        ├─→ CSV Processing
        ├─→ Log Processing
        └─→ API Processing
        ↓
Quality Check Validation Gate
        ↓
Elasticsearch Bulk Indexing
        ↓
Real-Time Analytics & Querying
```

## Configuration

### Modify DAG Schedule
Edit research_pipeline_dag.py:
```python
schedule_interval="0 2 * * *",  # Change execution time
```

### Adjust Retry Behavior
```python
default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}
```

### Scale Services
Edit docker-compose.yml to adjust resource limits and add additional services.

## Troubleshooting

### PostgreSQL Connection Error
```sh
docker-compose down -v
docker-compose up -d postgres
# Wait 30 seconds
docker-compose up -d
```

### Elasticsearch Won't Start
```sh
docker-compose logs elasticsearch
docker-compose restart elasticsearch
```

### DAG Not Appearing in Airflow
```sh
python -m py_compile dags/research_pipeline_dag.py
docker-compose restart airflow-scheduler
```

### Quality Check Failures
```sh
docker-compose exec airflow-webserver ls -la /opt/airflow/data/
docker-compose exec airflow-webserver cat /opt/airflow/data/processed_csv.json
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Test your changes thoroughly against ETL modules
4. Commit your changes (`git commit -m "Add feature description"`)
5. Push to the branch (`git push origin feature/improvement`)
6. Open a Pull Request

For major changes, please open an issue first to discuss your proposal.

## Performance Metrics

- **CSV ETL:** ~100 records/second
- **Log Processing:** ~50 records/second
- **Elasticsearch Indexing:** ~1000 docs/second
- **Quality Check:** <100ms

## License

This project is provided as-is for data engineering demonstration purposes.

## Support

For issues, questions, or improvements:
1. Check the Troubleshooting section
2. Review service logs: `docker-compose logs [service]`
3. Verify Docker container status: `docker-compose ps`
4. Check Airflow web UI for task execution details

---

**Last Updated:** April 2026  
**Status:** Production Ready  
**Version:** 1.0.0

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import timedelta
from airflow.utils.dates import days_ago

# 1. IMPORT YOUR ETL FUNCTIONS
from etl.etl_csv import ingest_csv
from etl.etl_logs import ingest_logs
from etl.etl_api import ingest_api
# We will create the es_loader and load_all function next!
from etl.es_loader import load_all 

default_args = {
    "owner": "data_engineering_team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "start_date": days_ago(1),
}

with DAG(
    "research_analytics_pipeline",
    default_args=default_args,
    schedule_interval="0 2 * * *",
    catchup=False
) as dag:

    # 2. REPLACE PLACEHOLDERS WITH ACTUAL COMMANDS
    
    # Pings Elasticsearch to make sure it is awake before starting
    check_es = BashOperator(
        task_id="check_elasticsearch_health", 
        bash_command="curl -s http://elasticsearch:9200 > /dev/null || exit 1"
    )

    ingest_csv_task = PythonOperator(
        task_id="ingest_transform_csv", 
        python_callable=ingest_csv
    )
    
    ingest_log_task = PythonOperator(
        task_id="ingest_transform_logs", 
        python_callable=ingest_logs
    )
    
    ingest_api_task = PythonOperator(
        task_id="ingest_transform_spotify_api",
        python_callable=ingest_api
    )

    # Runs the quality check script we still need to write
    quality = BashOperator(
        task_id="data_quality_check", 
        bash_command="python /opt/airflow/etl/quality_check.py"
    )

    load_es = PythonOperator(
        task_id="load_all_to_elasticsearch", 
        python_callable=load_all
    )

    # Simple terminal echo to confirm completion
    notify = BashOperator(
        task_id="pipeline_complete_notification", 
        bash_command='echo "Pipeline completely successfully!"'
    )

    # 3. SET THE DEPENDENCIES
    check_es >> [ingest_csv_task, ingest_log_task, ingest_api_task] >> quality >> load_es >> notify
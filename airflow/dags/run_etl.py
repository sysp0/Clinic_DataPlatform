import sys
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

sys.path.insert(0, '/opt/airflow')

from src import run

with DAG(
    dag_id='simple_etl_pipeline',
    start_date=datetime(2025, 12, 1),
    schedule='@hourly',
    default_args={
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
    },
    catchup=False
) as dag:
    
    etl_task = PythonOperator(
        task_id='run_etl',
        python_callable=run
    )
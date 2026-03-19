from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# 1. The Alarm Clock
my_dag = DAG(
    dag_id='volatility_watchdog_pipeline',
    start_date=datetime(2026, 3, 1), # Set in the past so it triggers immediately
    schedule_interval='@daily',
    catchup=False
)

# 2. Task 1: Run the Extraction Script
extract_and_load = BashOperator(
    task_id='run_load_script',
    bash_command='python /opt/airflow/scripts/load.py',
    dag=my_dag
)

# 3. Task 2: Run the Analytics Script
analyze_data = BashOperator(
    task_id='run_analytics_script',
    bash_command='python /opt/airflow/scripts/analytics.py',
    dag=my_dag
)

# 4. The Flow (Draw the arrow!)
extract_and_load >> analyze_data
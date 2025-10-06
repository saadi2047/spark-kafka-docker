from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'saadi',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 6),
    'retries': 0,
}

dag = DAG(
    'compare_tables_dag',
    default_args=default_args,
    description='Run Spark Table Comparison ETL',
    schedule_interval=None,  # manually triggered for POC
    catchup=False,
)

# Spark submit command inside docker-compose spark-master service
spark_submit_cmd = """
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages mysql:mysql-connector-java:8.0.33 \
  /opt/spark/work-dir/table_compare_etl.py
"""

run_spark_etl = BashOperator(
    task_id='run_table_comparison',
    bash_command=spark_submit_cmd,
    dag=dag,
)

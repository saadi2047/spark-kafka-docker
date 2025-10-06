from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'saadi',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 6),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# DAG definition
with DAG(
    dag_id='spark_kafka_mysql_dag',
    default_args=default_args,
    schedule_interval=None,  # manual trigger
    catchup=False,
    tags=['spark', 'kafka', 'mysql']
) as dag:

    run_spark_etl = BashOperator(
        task_id='run_spark_etl',
        bash_command="""
        docker exec spark-master /opt/spark/bin/spark-submit \
          --master spark://spark-master:7077 \
          --jars /opt/spark/jars/mysql-connector-j-8.0.33.jar,\
/opt/spark/jars/spark-sql-kafka-0-10_2.13-4.0.0.jar,\
/opt/spark/jars/spark-token-provider-kafka-0-10_2.13-4.0.0.jar,\
/opt/spark/jars/kafka-clients-3.7.0.jar \
          /opt/spark/work-dir/streaming-etl.py
        """
    )

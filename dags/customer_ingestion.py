
from airflow.models import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

import pendulum

spark_conf = {
    "spark.sql.parquet.int96RebaseModeInWrite": "CORRECTED",
}


dag_conf = {
    "dag_id": "dag1",
    "start_date": pendulum.today("UTC").add(days=-2),
    "schedule": "@once",
    "default_args": {"owner": "Umbrella Corp."},
}

with DAG(**dag_conf) as dag:
    t = SparkSubmitOperator(
        task_id="t1",
        application="jobs/start_t1.py",
        application_args=[],
    )

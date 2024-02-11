from airflow.models import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from typing import Union, List, Optional
from pathlib import Path
import re

import pendulum

spark_conf = {
    "spark.sql.parquet.int96RebaseModeInWrite": "CORRECTED",
}


vanilla_dag_conf = {
    "dag_id": "vanilla_dag",
    "start_date": pendulum.today("UTC").add(days=-2),
    "schedule": "@once",
    "default_args": {"owner": "Umbrella Corp."},
}

with DAG(**vanilla_dag_conf) as vanilla_dag:
    t = SparkSubmitOperator(
        task_id="t1",
        application="jobs/start.py",
        application_args=["data_ingest.ingestion1:main"],
        env_vars={"LOG_LEVEL": "DEBUG"},
        conn_id="spark_local",
    )


def create_spark_task(task_id: str, app: Union[str, Path], *, args: Optional[List[str]] = None, **kwargs):
    if isinstance(app, str) and re.search(r"^\w+(?:\.\w+)*:\w+$", app):
        args = [app] + (args or [])
        app = "jobs/start.py"

    return SparkSubmitOperator(
        application=str(app),
        application_args=args,
        task_id=task_id,
        **kwargs,
    )


dag_conf_cst = {
    "dag_id": "dag_cst",
    "start_date": pendulum.today("UTC").add(days=-2),
    "schedule": "@once",
    "default_args": {"owner": "Umbrella Corp."},
}

with DAG(**dag_conf_cst) as dag_cst:
    t = create_spark_task(
        "t1",
        "data_ingest.ingestion1:main",
        env_vars={"LOG_LEVEL": "DEBUG"},
        conn_id="spark_local",
    )

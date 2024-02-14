# :snippet vanilla_dag
from airflow.models import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# :cloak
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
# :endcloak

with DAG(**vanilla_dag_conf) as vanilla_dag:
    t = SparkSubmitOperator(
        task_id="t1",
        application="jobs/start.py",
        application_args=["data_ingest.ingestion1:main"],
        env_vars={"LOG_LEVEL": "DEBUG"},
        conn_id="spark_local",
    )
# :endsnippet

dag_conf_cst = {
    "dag_id": "dag_cst",
    "start_date": pendulum.today("UTC").add(days=-2),
    "schedule": "@once",
    "default_args": {"owner": "Umbrella Corp."},
}


# :snippet cst_dag
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


with DAG(**dag_conf_cst) as dag_cst:
    t = create_spark_task(
        "t1",
        "data_ingest.ingestion1:main",
        env_vars={"LOG_LEVEL": "DEBUG"},
        conn_id="spark_local",
    )
# :endsnippet

dag_conf_msso = {
    "dag_id": "dag_msso",
    "start_date": pendulum.today("UTC").add(days=-2),
    "schedule": "@once",
    "default_args": {"owner": "Umbrella Corp."},
}


# :snippet msso_dag
def MySparkSubmitOperator(application="", application_args=None, *args, **kwargs):
    if isinstance(application, str) and re.search(r"^\w+(?:\.\w+)*:\w+$", application):
        application_args = [application] + (application_args or [])
        application = "jobs/start.py"

    return SparkSubmitOperator(
        *args,
        application=str(application),
        application_args=application_args,
        **kwargs,
    )


with DAG(**dag_conf_msso) as dag_msso:
    t = MySparkSubmitOperator(
        task_id="t1",
        application="data_ingest.ingestion1:main",
        env_vars={"LOG_LEVEL": "DEBUG"},
        conn_id="spark_local",
    )
# :endsnippet

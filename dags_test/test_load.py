from pathlib import Path
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from airflow.models import DagBag

jobs_path = Path("./jobs")


def test_load(tmp_path, monkeypatch):
    dagbag = DagBag(dag_folder="dags", include_examples=False)
    for dag_id, dag in dagbag.dags.items():
        for task in dag.tasks:
            if isinstance(task, SparkSubmitOperator):
                assert task._application == "jobs/start.py"
    assert dagbag.size() >= 1

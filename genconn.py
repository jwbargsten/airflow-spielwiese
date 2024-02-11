from airflow.models.connection import Connection

c = Connection(
    conn_id="spark_local",
    conn_type="spark",
    host="local[2]",
    extra='{"queue": "root.default"}',
)


print(f"AIRFLOW_CONN_{c.conn_id.upper()}='{c.as_json()}'")

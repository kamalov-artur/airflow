from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="wait_for_power_keepalive",
    start_date=datetime(2025, 12, 1),
    schedule_interval="*/10 * * * *",
    catchup=False,
) as dag:

    wait_for_ping = ExternalTaskSensor(
        task_id="wait_for_power_ping",
        external_dag_id="power_keepalive",
        external_task_id="ping",
        allowed_states=["success"],
        failed_states=["failed", "skipped"],
        poke_interval=60,
        timeout=10 * 60,
        mode="reschedule",
    )

    after_ping = PythonOperator(
        task_id="after_ping",
        python_callable=lambda: print("Сенсор отработал"),
    )

    wait_for_ping >> after_ping

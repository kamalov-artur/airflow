"""
Обращение к сайту на streamlit для пинга для поддержания его работоспособности
Запуск каждые 10 минут
"""

import requests

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

URL = "https://power-interactive-plot.streamlit.app/"


def ping_site():
    resp = requests.get(URL, timeout=60)
    resp.raise_for_status()


with DAG(
    dag_id="power_keepalive",
    start_date=datetime(2025, 11, 1),
    schedule="*/10 * * * *",
    catchup=False,
    max_active_runs=1,
    default_args=dict(retries=3),
    tags=["streamlit"],
) as dag:

    dag.doc_md = __doc__

    PythonOperator(
        task_id="ping",
        python_callable=ping_site,
    )

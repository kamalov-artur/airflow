"""
Обращение к сайту на render для пинга для поддержания его работоспособности
Запуск каждые 30 минут, падение при 4xx/5xx.
"""

import requests

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

URL = "https://alpha-beta-interactive-plot.onrender.com/"


def ping_site():
    resp = requests.get(URL, timeout=60)
    resp.raise_for_status()


with DAG(
    dag_id="alpha_beta_keepalive",
    start_date=datetime(2025, 11, 1),
    schedule="0 * * * *",
    catchup=False,
    max_active_runs=1,
    default_args=dict(retries=3),
    tags=["render"],
) as dag:

    dag.doc_md = """
    Пингует `URL` раз в час, падает при ошибке`4xx/5xx`.  
    """

    PythonOperator(
        task_id="ping",
        python_callable=ping_site,
    )

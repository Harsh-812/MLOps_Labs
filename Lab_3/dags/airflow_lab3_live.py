from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from src.live import (
    load_data,
    data_preprocessing,
    build_save_model,
    choose_k_and_finalize,
)

default_args = {
    "owner": "harshitha",
    "start_date": datetime(2025, 1, 15),
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="harshitha_lab3_kmeans_live",
    default_args=default_args,
    description="Lab 3: K-Means clustering on Facebook Live Sellers engagement",
    schedule_interval=None,
    catchup=False,
    tags=["lab3", "kmeans", "facebook-live"],
) as dag:

    t_load = PythonOperator(
        task_id="load_live_data",
        python_callable=load_data,
    )

    t_prep = PythonOperator(
        task_id="preprocess_engagement_features",
        python_callable=data_preprocessing,
        op_args=[t_load.output],
    )

    t_build = PythonOperator(
        task_id="compute_sse_and_silhouette",
        python_callable=build_save_model,
        op_args=[t_prep.output],
    )

    t_finalize = PythonOperator(
        task_id="choose_k_and_finalize_model",
        python_callable=choose_k_and_finalize,
        op_args=[t_build.output],
    )

    t_list = BashOperator(
        task_id="list_outputs",
        bash_command=(
            "echo '--- Working data ---' && "
            "ls -lh /opt/airflow/working_data && "
            "echo 'Chosen k:' && cat /opt/airflow/working_data/chosen_k.txt || true"
        ),
    )

    t_load >> t_prep >> t_build >> t_finalize >> t_list

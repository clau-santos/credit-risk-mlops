from airflow import DAG
from airflow.decorators import task

from datetime import datetime

from home_credit_feature_pipeline.tasks import _read_data_and_transform_abt
from utils.minio import MinioClient

with DAG(
    dag_id="home_credit_feature_pipeline",
    description="Dag responsável por realizar a criação dos dados da ABT.",
    max_active_tasks=1,
    schedule=None,
    start_date=datetime(2026, 7, 12),
    catchup=False,
    max_active_runs = 1

) as dag:



    @task
    def read_data_and_transform_abt(var=None, ti=None):
        data = _read_data_and_transform_abt(var=var)
        ti.xcom_push(key="abt_data", value=data)

    @task
    def save_abt(var=None, ti=None):
        data = ti.xcom_pull(task_ids="read_data_and_transform_abt", key="abt_data")
        file_name = "abt.csv"

        minio_client = MinioClient(var=var, bucket_suffix="GOLD")
        minio_client.save_data(file_name=file_name, data=data)

    t1 = read_data_and_transform_abt()
    t2 = save_abt()

    t1 >> t2

if __name__ == "__main__":
    dag.test()

from airflow import DAG
from airflow.decorators import task

from datetime import datetime, UTC

from utils.minio import MinioClient

from Model.train import main
with DAG(
    dag_id="home_credit_model",
    description="Dag responsável por realizar a criação dos dados da ABT.",
    max_active_tasks=1,
    schedule=None,
    start_date=datetime(2026, 7, 12),
    catchup=False,
    max_active_runs = 1

) as dag:

    @task
    def read_data_and_model_train(var=None):
        minio_client = MinioClient(var=var, bucket_suffix="GOLD")
        data = minio_client.read_data_from_bucket(file_name="abt.csv")
        main(df=data)


    t1 = read_data_and_model_train()


    t1

if __name__ == "__main__":
    dag.test()

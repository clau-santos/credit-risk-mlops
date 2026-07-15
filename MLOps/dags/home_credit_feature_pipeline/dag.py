from airflow import DAG
from airflow.decorators import task
from airflow.operators.trigger_dagrun import trigger_dag


from datetime import datetime, UTC

from home_credit_feature_pipeline.tasks import _read_data_and_transform_abt, _save_abt

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
        _save_abt(data=data, var=var)


    @task
    def trigger_model_dag():
        trigger_dag(
            dag_id="home_credit_model",
            run_id=str(datetime.now(UTC).isoformat()),
            conf=None,
        )

    t1 = read_data_and_transform_abt()
    t2 = save_abt()
    t3 = trigger_model_dag()

    t1 >> t2

if __name__ == "__main__":
    dag.test()

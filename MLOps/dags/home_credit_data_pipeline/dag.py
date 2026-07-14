from airflow import DAG, AirflowException
from airflow.operators.trigger_dagrun import trigger_dag

from airflow.decorators import task
from datetime import datetime, UTC


from home_credit_data_pipeline.tasks import (
    _get_and_save_data,
    _validade_raw_data,
    _data_transform_and_validation,
    _save_clean_data
)


with DAG(
        dag_id="home_credit_data_pipeline",
        description="Dag responsável por realizar a ingestão dos dados de Home-Credit",
        max_active_tasks=1,
        schedule=None,
        start_date=datetime(2026, 7, 11),
        catchup=False,
        max_active_runs=1

) as dag:

    @task
    def get_and_save_data(var=None):
        _get_and_save_data(var=var)


    @task
    def validate_raw_data(var=None):
        _validade_raw_data(var=var)


    @task
    def data_transform_and_validation(var=None, ti=None):
        data = _data_transform_and_validation(var=var)
        ti.xcom_push(key="clean_data", value=data)


    @task
    def save_clean_data(var=None, ti=None):
        data = ti.xcom_pull(task_ids="data_transform_and_validation", key="clean_data")
        _save_clean_data(data=data, var=var)

    @task
    def trigger_feature_engineering_dag():
        trigger_dag(
            dag_id="home_credit_feature_pipeline",
            run_id=str(datetime.now(UTC).isoformat()),
            conf=None,
        )


    t1 = get_and_save_data()
    t2 = validate_raw_data()
    t3 = data_transform_and_validation()
    t4 = save_clean_data()
    t5 = trigger_feature_engineering_dag()

    t1 >> t2 >> t3 >> t4 >> t5

if __name__ == "__main__":
    dag.test()

from airflow import AirflowException

import os
import pandas as pd
import kagglehub


from utils.minio import MinioClient
from DataPipeline.data_sanitization import _data_validation, _data_transform


def _get_and_save_data(var=None):
    os.environ["KAGGLE_USERNAME"] = var["value"].get("KAGGLE_USERNAME")
    os.environ["KAGGLE_KEY"] = var["value"].get("KAGGLE_KEY")

    path = kagglehub.competition_download("home-credit-default-risk", path="application_train.csv")
    data = pd.read_csv(path)

    minio_client = MinioClient(var=var, bucket_suffix="RAW")
    minio_client.save_data(file_name="raw.csv", data=data)


def _validade_raw_data(var=None):
    minio_client = MinioClient(var=var, bucket_suffix="RAW")
    data = minio_client.read_data_from_bucket(file_name="raw.csv")

    try:
        print("Iniciando validação do contrato de dados.")
        _data_validation(df=data, model="RAW", validate_row=True)
        print("Contrato de dados validado com sucesso!")
    except ValueError as e:
        raise AirflowException(
            f"Falha na validação dos dados da camada RAW, revise o contrato de dados: {str(e)}"
        )


def _data_transform_and_validation(var):
    minio_client = MinioClient(var=var, bucket_suffix="RAW")
    data = minio_client.read_data_from_bucket(file_name="raw.csv")
    data = _data_transform(df=data)

    print("Limpeza dos dados realizada com sucesso!")

    try:
        print("Iniciando validação do contrato de dados.")
        _data_validation(df=data, model="SILVER", validate_row=True)
        print("Contrato de dados validado com sucesso!")
    except Exception as e:
        raise AirflowException(
            f"Falha na validação dos dados da camada SILVER, revise o contrato de dados: {str(e)}"
        )

    return data


def _save_clean_data(data:pd.DataFrame, var=None):
    minio_client = MinioClient(var=var, bucket_suffix="SILVER")
    minio_client.save_data(file_name="clean_data.csv", data=data)



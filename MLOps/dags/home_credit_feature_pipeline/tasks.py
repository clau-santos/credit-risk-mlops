import pandas as pd

from utils.minio import MinioClient

from DataPipeline.abt_transform import abt_transform

def _read_data_and_transform_abt(var=None):
    minio_client = MinioClient(var=var, bucket_suffix="SILVER")
    data = minio_client.read_data_from_bucket(file_name="clean_data.csv")
    abt_data, _ = abt_transform(df=data)
    return abt_data


def _save_abt(data: pd.DataFrame, var):
    file_name = "abt.csv"

    minio_client = MinioClient(var=var, bucket_suffix="GOLD")
    minio_client.save_data(file_name=file_name, data=data)
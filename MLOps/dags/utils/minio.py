from minio import Minio
import io
import json


class MinioClient:
    def __init__(self, bucket_suffix: str, var=None):
        self.bucket_name = var["value"].get(f"MINIO_BUCKET_NAME_{bucket_suffix}")
        self.endpoint = var["value"].get("MINIO_ENDPOINT")
        self.access_key = var["value"].get("MINIO_ACCESS_KEY")
        self.secret_key = var["value"].get("MINIO_SECRET_KEY")

    def _client_minio(self):
        minio_client = Minio(
            endpoint=self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False,
        )
        return minio_client

    def save_data(self, data: dict, file_name: str):
        bucket_name = self.bucket_name
        minio_client = self._client_minio()

        json_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
        file_path = f"{file_name}.csv"

        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' criado com sucesso!")

        try:
            minio_client.put_object(
                bucket_name=bucket_name,
                object_name=file_path,
                data=io.BytesIO(json_data),
                length=len(json_data),
                content_type="application/json"
            )
        except Exception as any_exception:
            raise any_exception

    def read_data_from_bucket(self, file_name: str) -> dict:
        """
        Recupera os arquivos existentes em um bucket do minIO.
        """
        bucket_name = self.bucket_name
        minio_client = self._client_minio()

        file_path = f"{file_name}.csv"

        with minio_client.get_object(bucket_name=bucket_name, object_name=file_path) as d:
            data = json.load(d)

        return data
import pandas as pd
from minio import Minio
import io

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

    def save_data(self, data: pd.DataFrame, file_name: str):
        bucket_name = self.bucket_name
        minio_client = self._client_minio()

        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' criado com sucesso!")

        print("Iniciando criação do arquivo.")
        csv_buffer = io.StringIO()
        data.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode("utf-8")

        try:
            minio_client.put_object(
                bucket_name=bucket_name,
                object_name=file_name,
                data=io.BytesIO(csv_bytes),
                length=len(csv_bytes),
                content_type="text/csv",
            )
            print(f"Arquivo '{file_name}' criado com sucesso!")
        except Exception as any_exception:
            raise any_exception

    def read_data_from_bucket(self, file_name: str) -> pd.DataFrame:
        """
        Recupera os arquivos existentes em um bucket do minIO.
        """
        bucket_name = self.bucket_name
        minio_client = self._client_minio()

        print(f"Iniciando leitura do arquivo. {file_name}")
        with minio_client.get_object(bucket_name=bucket_name, object_name=file_name) as d:
            data = pd.read_csv(io.BytesIO(d.read()))

        return data
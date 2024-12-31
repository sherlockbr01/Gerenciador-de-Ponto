import boto3
from datetime import datetime
import os

def backup_to_s3(db_path, bucket_name):
    # Inicializa a sessão do S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )

    # Nome do arquivo de backup
    backup_filename = f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.db"

    # Cria o arquivo de backup no S3
    s3.upload_file(db_path, bucket_name, backup_filename)
    print(f"Backup {backup_filename} enviado para o bucket {bucket_name}")

# Caminho para o banco de dados SQLite
db_path = 'ponto.db'

# Nome do bucket no S3
bucket_name = 'seu-bucket-s3'

# Executa o backup
backup_to_s3(db_path, bucket_name)

import os
import logging

from sqlalchemy import create_engine

from sqlalchemy_utils import database_exists, create_database

from src import unzip_zip_files
from src import concat_json_files
from src import ingest_payments
from src import ingest_originations
from src import bad_payer


logging.getLogger().setLevel(logging.INFO)

INGEST_PATH = ".ingest-data"

POSTGRESQL_DATABASE = os.getenv("POSTGRESQL_DATABASE", "CODE_CHALLENGE")
POSTGRESQL_IP = os.getenv("POSTGRESQL_IP", "127.0.0.1")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT", "5432")
POSTGRESQL_USERNAME = os.getenv("POSTGRESQL_USERNAME", "postgres")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD", "password")

engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
    POSTGRESQL_USERNAME,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_IP,
    POSTGRESQL_PORT,
    POSTGRESQL_DATABASE
))

# Criando database se caso não exista ainda.
if not database_exists(engine.url):
    create_database(engine.url)

# Lista dos arquivos para processar, poderia vir via argumentos de comando
files = [
    'originations.zip',
    'payments.zip',
]


def run():
    # Unzipa os arquivos primeiro numa pasta temporaria
    unzip_files = unzip_zip_files(INGEST_PATH, files)

    # Concatena todos os arquivos json e salva na RAW para ocupar menos espaço,
    # No caso eu criei um arquivo unico, mas o correto seria particionar por tamanho ou por data
    for f in unzip_files:
        concat_json_files(INGEST_PATH, f)

    # Processa os arquivos json e salva na camada TRUSTED num parquet particionado por ano e mes
    # e na REFINED no Postgres, no banco as tabelas sempre são reescritas
    ingest_payments(engine, f"{INGEST_PATH}/raw/payments.json", f"{INGEST_PATH}/trusted/payments")
    ingest_originations(engine, f"{INGEST_PATH}/raw/originations.json", f"{INGEST_PATH}/trusted/originations")

    # Processa o PySpark salvando uma tabela no Postgres com a porcetagem e arquivos parquet com os pagamentos.
    bad_payer(f"{INGEST_PATH}/trusted/bad_payer")


if __name__ == '__main__':
    run()

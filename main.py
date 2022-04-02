# Read json files

# Put into a table into Postgres DB
import os
from sqlalchemy import create_engine

from sqlalchemy_utils import database_exists, create_database

from src import unzip_zip_files
from src import concat_json_files
from src import ingest_payments
from src import ingest_originations


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

if not database_exists(engine.url):
    create_database(engine.url)


def run():
    files = [
        'originations.zip',
        'payments.zip',
    ]

    unzip_files = unzip_zip_files(INGEST_PATH, files)

    for f in unzip_files:
        concat_json_files(INGEST_PATH, f)

    ingest_payments(engine, f"{INGEST_PATH}/raw/payments.json", f"{INGEST_PATH}/trusted/payments.parquet")
    ingest_originations(engine, f"{INGEST_PATH}/raw/originations.json", f"{INGEST_PATH}/trusted/originations.parquet")


if __name__ == '__main__':
    run()

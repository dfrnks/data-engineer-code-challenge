import logging
import pandas as pd

from pathlib import Path


def ingest_payments(engine, src, dst) -> None:
    """
    Processa o arquivo payments e gera um parquet para salvar na trusted e salva no banco.
    :param engine:
    :param src:
    :param dst:
    :return:
    """
    logging.info("Iniciando processo ingestão payments")

    df = pd.read_json(src, lines=True)

    df['paymentDate'] = df['paymentDate'].astype('datetime64[s]')
    df['paymentId'] = df['paymentId'].astype(str)
    df['installmentId'] = df['installmentId'].astype(str)

    logging.info("Inserindo na trusted")

    df['year'] = df['paymentDate'].dt.year
    df['month'] = df['paymentDate'].dt.month

    trusted_path = Path(dst)
    trusted_path.mkdir(parents=True, exist_ok=True)

    df.to_parquet(dst, partition_cols=['year', 'month'])

    df.drop(['year', 'month'], axis=1, inplace=True)

    logging.info("Inserindo na refined")

    df.to_sql(
        'payments',
        con=engine,
        index=False,
        if_exists='replace',
        method='multi',
        chunksize=50
    )

    logging.info("Finalizando processo ingestão payments")


def ingest_originations(engine, src, dst) -> None:
    """
    Processa o arquivo payments e gera um parquet para salvar na trusted e salva no banco.
    :param engine:
    :param src:
    :param dst:
    :return:
    """
    logging.info("Iniciando processo ingestão originations")

    df = pd.read_json(src, lines=True)

    df = df.explode('installments')

    df.reset_index(inplace=True, drop=True)

    df = pd.concat([
        df.drop(['installments'], axis=1),
        pd.json_normalize(df['installments'])
    ], axis=1)

    df['dueDate'] = df['dueDate'].astype('datetime64[s]')
    df['registerDate'] = df['registerDate'].astype('datetime64[s]')

    df['originationId'] = df['originationId'].astype(str)
    df['clientId'] = df['clientId'].astype(str)
    df['installmentId'] = df['installmentId'].astype(str)
    df['installmentValue'] = df['installmentValue'].astype(float)

    logging.info("Inserindo na trusted")

    df['year'] = df['registerDate'].dt.year
    df['month'] = df['registerDate'].dt.month

    trusted_path = Path(dst)
    trusted_path.mkdir(parents=True, exist_ok=True)

    df.to_parquet(dst, partition_cols=['year', 'month'])

    df.drop(['year', 'month'], axis=1, inplace=True)

    logging.info("Inserindo na refined")

    df.to_sql(
        'originations',
        con=engine,
        index=False,
        if_exists='replace',
        method='multi',
        chunksize=50
    )

    logging.info("Finalizando processo ingestão originations")

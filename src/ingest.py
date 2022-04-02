import json
import pandas as pd


def ingest_payments(engine, src, dst):

    df = pd.read_json(src, lines=True)

    df['paymentDate'] = df['paymentDate'].astype('datetime64[s]')
    df['paymentId'] = df['paymentId'].astype(str)
    df['installmentId'] = df['installmentId'].astype(str)

    df.to_parquet(dst)

    df.to_sql(
        'payments',
        con=engine,
        index=False,
        if_exists='replace',
        method='multi',
        chunksize=50
    )


def ingest_originations(engine, src, dst):

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

    df.to_parquet(dst)

    df.to_sql(
        'originations',
        con=engine,
        index=False,
        if_exists='replace',
        method='multi',
        chunksize=50
    )

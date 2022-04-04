import os
import logging

from pyspark.sql import SparkSession

from pyspark.sql.functions import *
from pyspark.sql.types import *

POSTGRESQL_DATABASE = os.getenv("POSTGRESQL_DATABASE", "CODE_CHALLENGE")
POSTGRESQL_IP = os.getenv("POSTGRESQL_IP", "127.0.0.1")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT", "5432")
POSTGRESQL_USERNAME = os.getenv("POSTGRESQL_USERNAME", "postgres")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD", "password")


def bad_payer(dst):
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL") \
        .config("spark.jars", "postgresql-42.3.3.jar") \
        .getOrCreate()

    url = "jdbc:postgresql://{}:{}/{}".format(
        POSTGRESQL_IP,
        POSTGRESQL_PORT,
        POSTGRESQL_DATABASE
    )

    logging.info("Connectando Spark no banco")

    payments = spark.read \
        .format("jdbc") \
        .option("url", url) \
        .option("dbtable", "payments") \
        .option("user", POSTGRESQL_USERNAME) \
        .option("password", POSTGRESQL_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .load()

    originations = spark.read \
        .format("jdbc") \
        .option("url", url) \
        .option("dbtable", "originations") \
        .option("user", POSTGRESQL_USERNAME) \
        .option("password", POSTGRESQL_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .load()

    logging.info("Buscando as tabelas do banco")

    df = originations.join(payments, on='installmentId', how='left')

    df = df.select(
        '*',
        when(
            col("paymentDate") > col("dueDate"),
            True
        ).when(
            col("paymentDate").isNull(),
            True
        ).otherwise(False).alias("bad_payer"),
        datediff(col("paymentDate"), col("dueDate")).alias("datediff_ever"),
        round(months_between(col("paymentDate"), col("dueDate"))).cast(IntegerType()).alias('monthdiff_ever'),
        datediff(current_date(), col("dueDate")).alias("datediff_over"),
        round(months_between(current_date(), col("dueDate"))).cast(IntegerType()).alias('monthdiff_over'),
    )

    df = df.select(
        '*',
        when(
            col("paymentDate").isNull(),
            concat(
                lit("over-"),
                (
                    when(
                        col("monthdiff_over") != 0,
                        col("datediff_over") % col("monthdiff_over")
                    ).otherwise(col("datediff_over"))
                ),
                lit("-mob-"),
                col("monthdiff_over")
            )
        ).otherwise(
            concat(
                lit("ever-"),
                (
                    when(
                        col("monthdiff_ever") != 0,
                        col("datediff_ever") % col("monthdiff_ever")
                    ).otherwise(col("datediff_ever"))
                ),
                lit("-mob-"),
                col("monthdiff_ever")
            )
        ).alias("rules")
    ).drop('datediff_ever', 'monthdiff_ever', 'datediff_over', 'monthdiff_over')

    rules = spark.createDataFrame(
        df.where(
            (col("dueDate") < current_date()) &
            (
                    (col("dueDate") < col("paymentDate")) |
                    col("paymentDate").isNull()
            )
        ).groupBy("rules").count().collect())

    logging.info("Salvando tabela `bad_payer_rules` no banco")

    rules.select(
        '*',
        round(
            (col('count') * 100) / df.where(col('bad_payer') == True).count(), 2
        ).alias('perc')
    ).withColumnRenamed('count', 'total')\
        .write.format("jdbc") \
        .option("url", url) \
        .option("dbtable", "bad_payer_rules") \
        .option("user", POSTGRESQL_USERNAME) \
        .option("password", POSTGRESQL_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .save(mode='overwrite')

    logging.info("Salvando parquet na trusted")

    df.write.parquet(dst, mode='overwrite', partitionBy='bad_payer')

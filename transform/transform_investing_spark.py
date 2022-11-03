import os

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from common.constants import BALANCE_ARRAY_COLS, INCOME_ARRAY_COLS
from common.arg_transform import get_transform_args


GROUP_COLS = ["stock_id", "page_name", "extraction_time"]


def get_pivoted_page_df(investing_df, page_name):
    page_df = (
        investing_df
        .filter(f"page_name == '{page_name}'")
        .groupBy(GROUP_COLS)
        .pivot("metric")
        .agg(F.coalesce(F.first("value")))
    )

    return page_df


def transform_date(df):
    df = (
        df
        .withColumn("date", F.concat("date_years", F.lit('/'), "date_days_months"))
        .drop("date_years", "date_days_months")
    )

    return df


def transform_money_units(df):
    df = (
        df
        .withColumn("factor", F.regexp_extract("money_units", ".+In (\w+) of*", 1))
        .withColumn("currency", F.regexp_extract("money_units", ".+In \w+ of (\w+).*", 1))
        .drop("money_units")
    )

    return df


def transform_from_arrays(df, array_cols):
    splitted_cols = [F.split(col, ',').alias(col) for col in array_cols]
    df = (
        df

        # allows handling `null` values
        .fillna("", subset=array_cols)

        .withColumn("z", F.explode(F.arrays_zip(*splitted_cols)))
        .drop(*array_cols)
        .select("*", "z.*")
        .drop("z")

        # set empty string values to actual `null` values
        .replace({"": None, "-": None}, subset=array_cols)
    )

    return df


def transform_investing(investing_df):
    general_df = (
        get_pivoted_page_df(investing_df, "general")
        .withColumn("price", F.regexp_replace("price", ",", ""))
        .withColumn("shares", F.regexp_replace("shares", ",", ""))
    )

    balance_df = get_pivoted_page_df(investing_df, "balance-sheet")
    balance_df = transform_money_units(balance_df)
    balance_df = transform_from_arrays(balance_df, BALANCE_ARRAY_COLS)
    balance_df = transform_date(balance_df)

    income_df = get_pivoted_page_df(investing_df, "income-statement")
    income_df = transform_money_units(income_df)
    income_df = transform_from_arrays(income_df, INCOME_ARRAY_COLS)
    income_df = transform_date(income_df)

    return {
        "balance": balance_df,
        "income": income_df,
        "general": general_df,
    }


def main(input_csv=None, output_dest=None, spark=None):

    (input_csv, output_dest) = get_transform_args(input_csv, output_dest)

    if spark == None:
        spark = (
            SparkSession
            .builder
            .master('local[*]')
            .appName('transform_investing')
            .getOrCreate()
        )

    investing_df = (
        spark.read.csv(input_csv, header=True)
        .filter("source_id == 'investing'")
        .drop("source_id")
    )
    page_df_dict = transform_investing(investing_df)
    date_basename = os.path.basename(input_csv)[0:10]

    for (page, df) in page_df_dict.items():
        output_path = os.path.join(output_dest, date_basename, page)
        df.write.csv(output_path, header=True)


if __name__ == "__main__":
    main()

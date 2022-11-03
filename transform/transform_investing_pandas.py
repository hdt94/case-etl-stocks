import numpy as np
import pandas as pd

from typing import List

from common.constants import BALANCE_ARRAY_COLS, INCOME_ARRAY_COLS


def get_pivoted_page_df(investing_df, page_name):
    page_df = (
        investing_df
        .query("page_name == @page_name")
        .pivot(columns="metric", values="value")
    )

    return page_df


def transform_date(df):
    df["date"] = (
        df["date_years"]
        .str.cat(df["date_days_months"], sep='/')
    )

    df = df.drop(columns=["date_years", "date_days_months"])

    return df


def transform_from_arrays(df, array_cols):
    def arrays_zip(s: pd.Series) -> List[List[str]]:
        """
        - each value of `s` is a list
        - each value of `s` is indexed by one array column name
        """
        # TODO try-except possible array-lengths mismatch for zipping

        isna = s.isna()
        if isna.any():
            temp_df = pd.DataFrame([f for f in zip(*s[~isna])],
                                   columns=isna[~isna].index)
            temp_df[isna[isna].index] = np.NaN
            list2d = temp_df[s.index].values.tolist()
        else:
            list2d = [z for z in zip(*s)]

        return list2d

    df = (
        df
        .drop(columns=array_cols)
        .assign(
            z=(
                df[array_cols]
                # here is a dataframe where each value is a comma-separated string list of values
                .apply(lambda s: s.str.split(','))
                # here is a dataframe where each value is a list object
                .apply(arrays_zip, axis=1)
                # here is a series where each value is one list2d (a list of lists)
            )
        )
        .explode("z")
        # exploded list2d resulted in a single list per row
    )
    df = pd.concat(
        [
            # casting single list values into series resulting in a dataframe
            df["z"].apply(lambda x: pd.Series(x, index=array_cols)),

            # select scalar columns
            df.drop(columns=["z"])
        ],
        axis=1
    )
    df[array_cols] = df[array_cols].replace("-", np.NaN)

    return df


def transform_money_units(df):
    re_df = (
        df
        ["money_units"]
        .str.extract(".+In (?P<factor>\w+) of (?P<currency>\w+).*")
    )
    df = pd.concat([df.drop(columns=["money_units"]), re_df], axis=1)

    return df


def transform_page_df(df, array_cols):
    df = transform_from_arrays(df, array_cols)
    df = transform_date(df)
    df = transform_money_units(df)


def transform_general_page(general_df):
    general_df = (
        general_df
        .assign(
            price=general_df["price"].str.replace(',', ''),
            shares=general_df["shares"].str.replace(',', ''),
        )
    )

    return general_df


def transform_income_page(income_df):
    income_df = transform_from_arrays(income_df, INCOME_ARRAY_COLS)
    income_df = transform_date(income_df)
    income_df = transform_money_units(income_df)


def main(input_csv=None, output_dest=None):
    (input_csv, output_dest) = get_transform_args(input_csv, output_dest)

    # reading


if __name__ == "__main__":
    main()

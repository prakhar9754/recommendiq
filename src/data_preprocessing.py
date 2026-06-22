"""
Data Preprocessing Module

Purpose:
Perform reusable data cleaning and preprocessing operations

"""

import pandas as pd


def convert_timestamp(
    df: pd.DataFrame,
    timestamp_column: str = "timestamp"
) -> pd.DataFrame:
    """
    Convert Unix timestamp (milliseconds)
    into datetime format.
    """

    df[timestamp_column] = pd.to_datetime(
    df[timestamp_column],
    unit="ms"
    )

    return df


def remove_duplicates(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Remove duplicate records.
    """

    df = df.drop_duplicates()

    return df


def check_missing_values(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Generate missing value summary.
    """

    missing_summary = pd.DataFrame({
        "missing_count": df.isnull().sum(),
        "missing_percentage":
        (
            df.isnull().sum()
            / len(df)
        ) * 100
    })

    return missing_summary


def validate_transaction_ids(
    events_df: pd.DataFrame
) -> None:
    """
    Validate transaction IDs.

    Missing transaction IDs are expected
    for view and addtocart events.
    """

    missing_count = (
        events_df["transactionid"]
        .isnull()
        .sum()
    )

    print(
        f"Missing Transaction IDs: "
        f"{missing_count}"
    )


def clean_category_tree(
    category_tree_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Handle root category parent IDs.
    """

    category_tree_df["parentid"] = (
        category_tree_df["parentid"]
        .fillna(-1)
    )

    return category_tree_df


def merge_item_properties(
    part1: pd.DataFrame,
    part2: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge item property files.
    """

    item_properties_df = pd.concat(
        [part1, part2],
        ignore_index=True
    )

    return item_properties_df


def validate_dataset(
    df: pd.DataFrame,
    dataset_name: str
) -> None:
    """
    Print dataset validation summary.
    """

    print(
        f"\nDataset: {dataset_name}"
    )

    print(
        f"Shape: {df.shape}"
    )

    print(
        "\nMissing Values:"
    )

    print(
        df.isnull().sum()
    )


def save_to_database(
    df: pd.DataFrame,
    table_name: str,
    engine
) -> None:
    """
    Save dataframe to MySQL table.
    """

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )

    print(
        f"Table '{table_name}' saved successfully."
    )
"""
Feature Engineering Module

Purpose:
Generate machine learning features from cleaned RetailRocket data.
"""

import pandas as pd

def create_interaction_strength(events_df: pd.DataFrame) -> pd.DataFrame: 
    #Input  : DataFrame
    #Output : DataFrame
 
    #Create weighted interaction strength. 
    event_weights = {
        "view": 1,
        "addtocart": 3,
        "transaction": 5
    }

    events_df["interaction_strength"] = (
        events_df["event"].map(event_weights)
    )

    return events_df


def create_recency_feature(
    events_df: pd.DataFrame
) -> pd.DataFrame:

    events_df["timestamp"] = pd.to_datetime(
        events_df["timestamp"]
    )

    max_date = events_df["timestamp"].max()

    events_df["recency_days"] = (
        max_date - events_df["timestamp"]
    ).dt.days

    return events_df


def create_user_features(events_df: pd.DataFrame) -> pd.DataFrame:
    
    #Generate user-level behavioral features.
    user_features = (
        events_df
        .groupby("visitorid")
        .agg(
            total_interactions=("visitorid", "count"),
            avg_interaction_strength=(
                "interaction_strength",
                "mean"
            )
        )
        .reset_index()
    )

    return user_features


def create_item_features(events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate item-level features.
    """

    item_features = (
        events_df
        .groupby("itemid")
        .agg(
            interaction_count=("itemid", "count"),
            avg_interaction_strength=(
                "interaction_strength",
                "mean"
            )
        )
        .reset_index()
    )

    return item_features


def create_user_item_features(
    events_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Create user-item interaction matrix features.
    """

    user_item_features = (
        events_df
        .groupby(["visitorid", "itemid"])
        .agg(
            interaction_strength=(
                "interaction_strength",
                "sum"
            ),
            recency_days=(
                "recency_days",
                "min"
            )
        )
        .reset_index()
    )

    return user_item_features


def build_feature_pipeline(
    events_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Main feature engineering pipeline.
    
    This is now producing:
    visitorid
    total_interactions
    avg_interaction_strength
    """


    events_df = create_interaction_strength(events_df)

    events_df = create_recency_feature(events_df)

    customer_features = create_user_features(
    events_df
     )
    return customer_features
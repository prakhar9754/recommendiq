"""
Feature Engineering Module

Purpose:
Generate machine learning features from cleaned RetailRocket data.
"""

import pandas as pd


def create_event_scores(events_df: pd.DataFrame) -> pd.DataFrame:

    #Encode event types into numerical scores.
    event_mapping = {
        "view": 1,
        "addtocart": 2,
        "transaction": 3
    }

    events_df["event_score"] = events_df["event"].map(event_mapping)

    return events_df


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


def create_recency_feature(events_df: pd.DataFrame) -> pd.DataFrame:
   
    #Create recency feature in days.
    events_df["datetime"] = pd.to_datetime(
        events_df["datetime"]
    )

    max_date = events_df["datetime"].max() #recent date

    events_df["recency_days"] = (
        max_date - events_df["datetime"]
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
    """

    events_df = create_event_scores(events_df)

    events_df = create_interaction_strength(events_df)

    events_df = create_recency_feature(events_df)

    final_features = create_user_item_features(
        events_df
    )

    return final_features
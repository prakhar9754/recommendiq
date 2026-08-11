"""
Service Layer

Purpose:
Contains the business logic for the RecommendIQ API.
"""

import pandas as pd
import joblib
from src import segmentation # type: ignore
from src import recommender #type:ignore


# --------------------------------------------------
# File Paths
# --------------------------------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CUSTOMER_FEATURES = BASE_DIR / "data" / "features" / "customer_features.csv"

USER_ITEM_FEATURES = BASE_DIR / "data" / "features" / "user_item_features.csv"

SEGMENTATION_PIPELINE = BASE_DIR / "artifacts" / "segmentation_pipeline.pkl"

SIMILARITY_MODEL = BASE_DIR / "artifacts" / "item_similarity.pkl"


# --------------------------------------------------
# Get Customer Segment
# --------------------------------------------------

def get_customer_segment(visitorid: int):
    """
    Predict customer segment.
    """

    # Load customer features
    customer_df = segmentation.load_customer_features(
        CUSTOMER_FEATURES
    )

    # Load segmentation pipeline
    pipeline = joblib.load(
        SEGMENTATION_PIPELINE
    )

    # Find customer
    customer = customer_df[
        customer_df["visitorid"] == visitorid
    ]

    if customer.empty:
        return None

    # Remove ID column
    features = customer.drop(columns=["visitorid"])

    # Predict cluster
    cluster = pipeline.predict(features)[0]

    # Map cluster number to name
    cluster_mapping = {
        0: "Browsers",
        1: "Inactive",
        2: "Regular Users",
        3: "Buyers",
        4: "Cart Users"
    }

    segment = cluster_mapping.get(
        cluster,
        "Unknown"
    )

    return {
        "visitorid": visitorid,
        "cluster": int(cluster),
        "customer_segment": segment
    }


# --------------------------------------------------
# Existing Customer Recommendation
# --------------------------------------------------

def get_recommendations(
    visitorid: int,
    top_n: int = 10
):
    """
    Generate personalized recommendations.
    If personalized recommendations are unavailable,
    return popular items instead.
    """

    # Load interaction data
    interaction_df = recommender.load_interaction_data(
        USER_ITEM_FEATURES
    )

    # Load item similarity model
    similarity_df = recommender.load_recommender(
        SIMILARITY_MODEL
    )

    # Try personalized recommendations
    recommendations = (
        recommender.recommend_for_existing_user(
            visitorid=visitorid,
            interaction_df=interaction_df,
            similarity_df=similarity_df,
            top_n=top_n
        )
    )

    # If personalized recommendations are empty,
    # use popular items
    if not recommendations:

        recommendations = (
            recommender.recommend_for_new_user(
                interaction_df,
                top_n=top_n
            )
        )

    return {
        "visitorid": visitorid,
        "recommendations": recommendations
    }
# --------------------------------------------------
# Popular Recommendations
# --------------------------------------------------

def get_popular_items(top_n: int = 10):
    """
    Recommend popular items.
    """

    interaction_df = recommender.load_interaction_data(
        USER_ITEM_FEATURES
    )

    recommendations = (
        recommender.recommend_for_new_user(
            interaction_df,
            top_n=top_n
        )
    )

    return {
        "recommendations": recommendations
    }
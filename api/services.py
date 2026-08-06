"""
Service Layer

Purpose:
Contains the business logic for the RecommendIQ API.
"""

import pandas as pd

from src import segmentation # type: ignore
from src import recommender #type:ignore


# --------------------------------------------------
# File Paths
# --------------------------------------------------

CUSTOMER_FEATURES = "../data/features/customer_features.csv"

USER_ITEM_FEATURES = "../data/features/user_item_features.csv"

SEGMENT_MODEL = "../artifacts/kmeans_model.pkl"

SCALER_MODEL = "../artifacts/scaler.pkl"

SIMILARITY_MODEL = "../artifacts/item_similarity.pkl"


# --------------------------------------------------
# Get Customer Segment
# --------------------------------------------------

def get_customer_segment(visitorid: int):
    """
    Predict customer segment.
    """

    customer_df = segmentation.load_customer_features(
        CUSTOMER_FEATURES
    )

    scaler, kmeans = segmentation.load_models(
        scaler_path=SCALER_MODEL,
        model_path=SEGMENT_MODEL
    )

    customer = customer_df[
        customer_df["visitorid"] == visitorid
    ]

    if customer.empty:
        return None

    features = customer.drop(columns=["visitorid"])

    cluster, segment = segmentation.predict_customer_segment(
        features,
        scaler,
        kmeans
    )

    return {
        "visitorid": visitorid,
        "cluster": cluster,
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
    Generate recommendations.
    """

    interaction_df = recommender.load_interaction_data(
        USER_ITEM_FEATURES
    )

    similarity_df = recommender.load_recommender(
        SIMILARITY_MODEL
    )

    recommendations = (
        recommender.recommend_for_existing_user(
            visitorid=visitorid,
            interaction_df=interaction_df,
            similarity_df=similarity_df,
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
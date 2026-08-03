"""
This module contains reusable functions for customer segmentation
using K-Means clustering.
"""

import pandas as pd
import joblib

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def load_customer_features(filepath):
    """
    Load customer feature dataset.
    """

    try:
        customer_df = pd.read_csv(filepath)

        print("=" * 50)
        print("Customer features loaded successfully.")
        print(f"Number of rows    : {customer_df.shape[0]}")
        print(f"Number of columns : {customer_df.shape[1]}")
        print("=" * 50)

        return customer_df

    except FileNotFoundError:
        print(f"Error: File not found -> {filepath}")
        return None

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None

def preprocess_features(customer_df):
    """
    Prepare customer features for K-Means clustering.
    """

    # Copy dataframe
    df = customer_df.copy()

    # Remove identifier column
    if "visitorid" in df.columns:
        df = df.drop(columns=["visitorid"])

    # Initialize scaler
    scaler = StandardScaler()

    # Scale all features
    X_scaled = scaler.fit_transform(df)

    print("=" * 50)
    print("Feature preprocessing completed.")
    print(f"Number of samples : {X_scaled.shape[0]}")
    print(f"Number of features: {X_scaled.shape[1]}")
    print("=" * 50)

    return X_scaled, scaler

def train_kmeans(X_scaled, n_clusters=5, random_state=42):
    """
    Train a K-Means clustering model.
    """

    # Initialize K-Means model
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10
    )

    # Train model
    kmeans.fit(X_scaled)

    print("=" * 50)
    print("K-Means model trained successfully.")
    print(f"Number of clusters : {n_clusters}")
    print(f"Inertia            : {kmeans.inertia_:.2f}")
    print("=" * 50)

    return kmeans

def assign_clusters(customer_df, kmeans, X_scaled):
    """
    Assign cluster labels to customers.add cluster column in df 

    """

    # Create a copy of dataframe
    segmented_df = customer_df.copy()

    # Predict cluster for every customer
    segmented_df["cluster"] = kmeans.predict(X_scaled)

    print("=" * 50)
    print("Cluster assignment completed.")
    print(f"Total customers : {len(segmented_df)}")
    print(f"Clusters found  : {segmented_df['cluster'].nunique()}")
    print("=" * 50)

    return segmented_df

def map_cluster_names(segmented_df):
    """
    Map cluster numbers to meaningful customer segment names.
    """

    # Cluster mapping
    cluster_mapping = {
        0: "Browsers",
        1: "Inactive",
        2: "Regular Users",
        3: "Buyers",
        4: "Cart Users"
    }

    # Create a copy
    final_df = segmented_df.copy()

    # Map cluster numbers to names
    final_df["customer_segment"] = final_df["cluster"].map(cluster_mapping)

    print("=" * 50)
    print("Customer segment names assigned successfully.")
    print("=" * 50)

    return final_df

def save_models(scaler, kmeans,
                scaler_path="../artifacts/scaler.pkl",
                model_path="../artifacts/kmeans_model.pkl"):
    """
    Save the trained scaler and K-Means model.
    Returns
    -------
    None
    """

    # Save scaler
    joblib.dump(scaler, scaler_path)

    # Save K-Means model
    joblib.dump(kmeans, model_path)

    print("=" * 50)
    print("Models saved successfully.")
    print(f"Scaler saved at : {scaler_path}")
    print(f"KMeans saved at : {model_path}")
    print("=" * 50)

def load_models(
    scaler_path="../artifacts/scaler.pkl",
    model_path="../artifacts/kmeans_model.pkl"
):
    """
    Load the saved StandardScaler and K-Means model.
    """

    # Load scaler
    scaler = joblib.load(scaler_path)

    # Load K-Means model
    kmeans = joblib.load(model_path)

    print("=" * 50)
    print("Models loaded successfully.")
    print(f"Scaler loaded from : {scaler_path}")
    print(f"KMeans loaded from : {model_path}")
    print("=" * 50)

    return scaler, kmeans

def predict_customer_segment(customer_features, scaler, kmeans):
    """
    Predict customer segment for new customer data.
    """

    # Cluster mapping
    cluster_mapping = {
        0: "Browsers",
        1: "Inactive",
        2: "Regular Users",
        3: "Buyers",
        4: "Cart Users"
    }

    # Scale customer features
    customer_scaled = scaler.transform(customer_features)

    # Predict cluster
    cluster = kmeans.predict(customer_scaled)[0]

    # Convert cluster number to name
    segment_name = cluster_mapping.get(cluster, "Unknown")

    print("=" * 50)
    print("Customer segment predicted successfully.")
    print(f"Cluster Number : {cluster}")
    print(f"Customer Segment : {segment_name}")
    print("=" * 50)

    return cluster, segment_name

def segment_summary(segmented_df):
    """
    Generate summary statistics for customer segments.
    returns:   Summary of customer segments.
    """

    # Count customers in each segment
    summary_df = (
        segmented_df["customer_segment"]
        .value_counts()
        .reset_index()
    )

    # Rename columns
    summary_df.columns = [
        "Customer Segment",
        "Number of Customers"
    ]

    # Calculate percentage
    summary_df["Percentage"] = (
        summary_df["Number of Customers"]
        / summary_df["Number of Customers"].sum()
        * 100
    ).round(2)

    print("=" * 50)
    print("Customer Segment Summary")
    print("=" * 50)

    print(summary_df)

    return summary_df
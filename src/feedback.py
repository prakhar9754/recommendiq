import os
import joblib
import pandas as pd
import numpy as np

def load_feedback_data(file_path):
    """
    Load customer feedback data.
    
    """

    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Feedback file not found: {file_path}"
        )

    # Load dataset
    feedback_df = pd.read_csv(file_path)

    print("=" * 50)
    print("Feedback data loaded successfully.")
    print(f"Number of records : {len(feedback_df)}")
    print(f"Number of columns : {feedback_df.shape[1]}")
    print("=" * 50)

    return feedback_df

def preprocess_feedback(feedback_df):
    """
    Clean and standardize customer feedback.
    
    """

    # Create a copy to avoid modifying original data
    feedback_df = feedback_df.copy()

    # Fill missing feedback
    feedback_df["feedback"] = (
        feedback_df["feedback"]
        .fillna("No Feedback")
    )

    # Remove extra spaces
    feedback_df["feedback"] = (
        feedback_df["feedback"]
        .str.strip()
    )

    # Convert to Title case
    feedback_df["feedback"] = (
        feedback_df["feedback"]
        .str.title()
    )

    print("=" * 50)
    print("Feedback preprocessing completed.")
    print(f"Total records : {len(feedback_df)}")
    print("=" * 50)

    return feedback_df

def encode_feedback(feedback_df):
    """
    Convert text feedback into numerical scores.

    """

    # Create a copy
    feedback_df = feedback_df.copy()

    # Feedback mapping
    feedback_mapping = {
        "Like": 1,
        "Neutral": 0,
        "Dislike": -1,
        "No Feedback": 0
    }

    # Encode feedback
    feedback_df["feedback_score"] = (
        feedback_df["feedback"]
        .map(feedback_mapping)
    )

    print("=" * 50)
    print("Feedback encoding completed.")
    print("Feedback successfully converted to numerical scores.")
    print("=" * 50)

    return feedback_df

def update_recommendation_scores(
    feedback_df,
    learning_rate=0.10
):
    """
    Update recommendation scores using customer feedback.

    """

    # Create a copy
    feedback_df = feedback_df.copy()

    # Update recommendation score
    feedback_df["updated_score"] = (
        feedback_df["recommendation_score"]
        + learning_rate * feedback_df["feedback_score"]
    ) 

    # Keep scores between 0 and 1
    feedback_df["updated_score"] = np.clip(
        feedback_df["updated_score"],
        0,
        1
    )

    print("=" * 50)
    print("Recommendation scores updated successfully.")
    print(f"Learning Rate : {learning_rate}")
    print("=" * 50)

    return feedback_df

def rerank_recommendations(feedback_df):
    """
    Re-rank recommendations using updated scores.
    """

    # Create a copy
    feedback_df = feedback_df.copy()

    # Sort recommendations
    feedback_df = feedback_df.sort_values(
        by=["visitorid", "updated_score"],
        ascending=[True, False]
    )

    # Assign new ranking
    feedback_df["updated_rank"] = (
        feedback_df
        .groupby("visitorid")
        .cumcount()
        + 1
    )

    print("=" * 50)
    print("Recommendations re-ranked successfully.")
    print("=" * 50)

    return feedback_df

def feedback_summary(feedback_df):
    """
    Display summary statistics of customer feedback.
    """

    # Count each feedback type
    summary = feedback_df["feedback"].value_counts()

    print("=" * 50)
    print("Feedback Summary")
    print("=" * 50)

    print(f"Total Records : {len(feedback_df)}")

    print(f"Likes         : {summary.get('Like', 0)}")
    print(f"Neutral       : {summary.get('Neutral', 0)}")
    print(f"Dislikes      : {summary.get('Dislike', 0)}")
    print(f"No Feedback   : {summary.get('No Feedback', 0)}")

    print("=" * 50)

    return summary

def save_feedback_data(feedback_df, file_path):
    """
    Save processed feedback dataframe.
    """

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save dataframe
    feedback_df.to_csv(file_path, index=False)

    print("=" * 50)
    print("Feedback data saved successfully.")
    print(f"Saved to : {file_path}")
    print("=" * 50)
    
def load_feedback_data_file(file_path):
    """
    Load processed feedback dataframe.
    """

    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Processed feedback file not found: {file_path}"
        )

    # Load dataframe
    feedback_df = pd.read_csv(file_path)

    print("=" * 50)
    print("Processed feedback loaded successfully.")
    print(f"Number of records : {len(feedback_df)}")
    print(f"Number of columns : {feedback_df.shape[1]}")
    print("=" * 50)

    return feedback_df






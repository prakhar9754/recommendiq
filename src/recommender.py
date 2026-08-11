import os
import joblib
import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

def load_interaction_data(file_path):
    """
    Load customer interaction data for recommendation.
    
    """

    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Interaction file not found: {file_path}"
        )

    # Load dataset
    interaction_df = pd.read_csv(file_path)

    print("=" * 50)
    print("Interaction data loaded successfully.")
    print(f"Number of interactions : {len(interaction_df)}")
    print(f"Number of columns      : {interaction_df.shape[1]}")
    print("=" * 50)

    return interaction_df

def create_interaction_matrix(interaction_df, max_rows=10000):
    """
    Create a smaller user-item interaction matrix
    to avoid memory errors.
    """

    # Take only 10,000 interactions
    if len(interaction_df) > max_rows:
        interaction_df = interaction_df.sample(
            n=max_rows,
            random_state=42
        )

    print("=" * 50)
    print("Creating interaction matrix")
    print(f"Interactions used : {len(interaction_df)}")
    print(
        f"Unique users      : "
        f"{interaction_df['visitorid'].nunique()}"
    )
    print(
        f"Unique items      : "
        f"{interaction_df['itemid'].nunique()}"
    )
    print("=" * 50)

    interaction_matrix = interaction_df.pivot_table(
        index="visitorid",
        columns="itemid",
        values="interaction_strength",
        fill_value=0
    )

    print("=" * 50)
    print("Interaction matrix created successfully.")
    print(f"Users  : {interaction_matrix.shape[0]}")
    print(f"Items  : {interaction_matrix.shape[1]}")
    print("=" * 50)

    return interaction_matrix

def train_similarity_model(interaction_matrix):
    """
    Train an item-item similarity model using cosine similarity."""

    # Calculate cosine similarity between items
    similarity = cosine_similarity(interaction_matrix.T)

    # Convert to DataFrame
    similarity_df = pd.DataFrame(
        similarity,
        index=interaction_matrix.columns,
        columns=interaction_matrix.columns
    )

    print("=" * 50)
    print("Item similarity model trained successfully.")
    print(f"Number of items : {similarity_df.shape[0]}")
    print("=" * 50)

    return similarity_df

def recommend_items(visitorid,
                    interaction_df,
                    similarity_df,
                    top_n=10):
    """
    Recommend items for an existing customer.
    
    Parameters
    ----------
    visitorid : int
        Customer ID.

    interaction_df : pandas.DataFrame
        Customer interaction data.

    similarity_df : pandas.DataFrame
        Item-item similarity matrix.

    top_n : int
        Number of recommendations.
    """

    # Find items already interacted with
    interacted_items = interaction_df[
        interaction_df["visitorid"] == visitorid
    ]["itemid"].unique()

    # Customer not found:new customer
    if len(interacted_items) == 0:
        print("Customer has no interaction history.")
        return []

    # Dictionary to store recommendation scores
    recommendation_scores = {} #Item : Score

    # Calculate recommendation scores
    for item in interacted_items:

        if item not in similarity_df.index:
            continue

        similar_items = similarity_df[item]

        for similar_item, score in similar_items.items():

            if similar_item in interacted_items:
                continue

            recommendation_scores[similar_item] = (
                recommendation_scores.get(similar_item, 0)
                + score
            )

    # Sort recommendations
    recommendations = sorted(
        recommendation_scores.items(),
        key=lambda x: x[1], #x[0] = item,x[1] = recommendation score 
        #sort using x[1] = recommendation score
        reverse=True
    )

    # Return Top-N item IDs
    recommended_items = [
        item
        for item, score in recommendations[:top_n]
    ]

    print("=" * 50)
    print("Recommendations generated successfully.")
    print(f"Customer ID : {visitorid}")
    print(f"Recommended Items : {len(recommended_items)}")
    print("=" * 50)
#returns python list 
    return recommended_items

#What should we recommend to a brand-new customer who has no interaction history?
def recommend_popular_items(interaction_df, top_n=10):
    """
    Recommend the most popular items.
    """

    # Count interactions for each item
    popular_items = (
        interaction_df
        .groupby("itemid")["interaction_strength"]
        .sum()
        .sort_values(ascending=False)
    )

    # Get Top-N item IDs
    recommended_items = popular_items.head(top_n).index.tolist() #Pandas Index = Python list.

    print("=" * 50)
    print("Popular recommendations generated successfully.")
    print(f"Number of recommendations : {len(recommended_items)}")
    print("=" * 50)

    return recommended_items

def filter_seen_items(visitorid,
                      interaction_df,
                      recommended_items):
    """
    Remove items already interacted with by the customer.

    """

    # Get customer's interacted items
    seen_items = interaction_df[
        interaction_df["visitorid"] == visitorid
    ]["itemid"].unique()

    # Remove already seen items
    filtered_items = [
        item
        for item in recommended_items
        if item not in seen_items
    ]

    print("=" * 50)
    print("Seen items removed successfully.")
    print(f"Original Recommendations : {len(recommended_items)}")
    print(f"Filtered Recommendations : {len(filtered_items)}")
    print("=" * 50)

    return filtered_items

def save_recommender(similarity_df,
                     model_path="../artifacts/item_similarity.pkl"):
    """
    Save the item similarity matrix.

    """

    # Create artifacts folder if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Save similarity matrix
    joblib.dump(similarity_df, model_path)

    print("=" * 50)
    print("Recommendation model saved successfully.")
    print(f"Saved at : {model_path}")
    print("=" * 50)
    
def load_recommender(model_path="../artifacts/item_similarity.pkl"):
    """
    Load the saved item similarity matrix.
    """

    # Check if model exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Recommendation model not found: {model_path}"
        )

    # Load similarity matrix
    similarity_df = joblib.load(model_path)

    print("=" * 50)
    print("Recommendation model loaded successfully.")
    print(f"Loaded from : {model_path}")
    print("=" * 50)

    return similarity_df

def recommend_for_new_user(interaction_df, top_n=10):
    """
    Recommend products for a new customer.
    """

    print("=" * 50)
    print("New customer detected.")
    print("Generating popular recommendations...")
    print("=" * 50)

    recommendations = recommend_popular_items(
        interaction_df=interaction_df,
        top_n=top_n
    )

    return recommendations

def recommend_for_existing_user(visitorid,
                                interaction_df,
                                similarity_df,
                                top_n=10):
    """
    Generate personalized recommendations for an existing customer.

    """

    print("=" * 50)
    print(f"Generating recommendations for Customer {visitorid}")
    print("=" * 50)

    # Generate recommendations
    recommendations = recommend_items(
        visitorid=visitorid,
        interaction_df=interaction_df,
        similarity_df=similarity_df,
        top_n=top_n * 2
    )

    # Remove already seen items
    recommendations = filter_seen_items(
        visitorid=visitorid,
        interaction_df=interaction_df,
        recommended_items=recommendations
    )

    # Return only Top-N recommendations
    recommendations = recommendations[:top_n]

    print("=" * 50)
    print("Personalized recommendations ready.")
    print(f"Returned {len(recommendations)} recommendations.")
    print("=" * 50)

    return recommendations


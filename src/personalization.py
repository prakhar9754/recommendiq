'''
==========================================================
 Personalization Engine
 ==========================================================
 '''

import pandas as pd
import numpy as np


class PersonalizationEngine:
    """
    Personalization Engine
    Adjusts recommendation scores based on user feedback
    and user preferences.
    """

    def __init__(self):
        """Initialize personalization engine."""
        pass
    
    def load_recommendations(self, file_path):
        """
        Load recommendation data from CSV.
        """
        recommendations = pd.read_csv(file_path)

        print(f"Loaded {len(recommendations)} recommendations.")

        return recommendations
    
    def calculate_user_preferences(self, recommendations):
        """
        Calculate user preference statistics.
        """

        user_preferences = recommendations.groupby("visitorid").agg({
        "recommendation_score": "mean",
        "updated_score": "mean",
        "feedback_score": "mean"
        }).reset_index()

        return user_preferences
    
    def calculate_personalization_score(
    self,
    recommendations,
    user_preferences
    ):
        """
        Calculate personalized recommendation scores.
        """

        personalized = recommendations.merge(
        user_preferences,
        on="visitorid",
        suffixes=("", "_user")
        )

        personalized["personalization_score"] =
        (
        0.60 * personalized["updated_score"] +
        0.25 * personalized["feedback_score_user"] +
        0.15 * personalized["updated_score_user"]
        )

        personalized["personalization_score"] = (
        personalized["personalization_score"]
        .clip(0, 1)
        )

        return personalized
    
    def rank_recommendations(self, personalized):
        """
        Rank personalized recommendations for each user.
        """

        personalized = personalized.sort_values(
        ["visitorid", "personalization_score"],
        ascending=[True, False]
        )

        personalized["personalized_rank"] = (
        personalized.groupby("visitorid")
        .cumcount() + 1
        )

        return personalized
    
    def save_personalized_recommendations(
    self,
    personalized,
    output_path
):
        """
        Save personalized recommendations to CSV.
        """
        personalized.to_csv(output_path, index=False)

        print(f"Personalized recommendations saved to {output_path}")
        
    def run(self, input_path, output_path):
        """
        Run the complete personalization pipeline.
        """

        recommendations = self.load_recommendations(input_path)

        user_preferences = self.calculate_user_preferences(
        recommendations
        )

        personalized = self.calculate_personalization_score(
        recommendations,
        user_preferences
        )

        personalized = self.rank_recommendations(
        personalized
        )

        self.save_personalized_recommendations(
        personalized,
        output_path
        )

        print("Personalization pipeline completed successfully.")
    
    
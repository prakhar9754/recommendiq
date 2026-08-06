"""
Pydantic Schemas

Purpose:
Define request and response models for the RecommendIQ API.
"""

from pydantic import BaseModel
from typing import List


# ----------------------------------------------------
# Request Schema
# ----------------------------------------------------

class VisitorRequest(BaseModel):
    """
    Request model containing a visitor ID.
    """

    visitorid: int


# ----------------------------------------------------
# Recommendation Response
# ----------------------------------------------------

class RecommendationResponse(BaseModel):
    """
    Response model for recommendations.
    """

    visitorid: int
    recommendations: List[int]


# ----------------------------------------------------
# Customer Segment Response
# ----------------------------------------------------

class SegmentResponse(BaseModel):
    """
    Response model for customer segmentation.
    """

    visitorid: int
    cluster: int
    customer_segment: str


# ----------------------------------------------------
# Feedback Request
# ----------------------------------------------------

class FeedbackRequest(BaseModel):
    """
    Request model for customer feedback.
    """

    visitorid: int
    itemid: int
    feedback: str


# ----------------------------------------------------
# Success Response
# ----------------------------------------------------

class MessageResponse(BaseModel):
    """
    Generic success response.
    """

    message: str
"""
API Routes

Purpose:
Define all API endpoints for the RecommendIQ project.
"""

from fastapi import APIRouter, HTTPException

from api.services import ( #type:ignore
    get_customer_segment,
    get_recommendations,
    get_popular_items
)

from api.schemas import ( #type:ignore
    RecommendationResponse,
    SegmentResponse
)

router = APIRouter()


# --------------------------------------------------
# Home Endpoint
# --------------------------------------------------

@router.get("/")
def home():
    """
    Health check endpoint.
    """

    return {
        "message": "RecommendIQ API is running successfully."
    }


# --------------------------------------------------
# Customer Segment
# --------------------------------------------------

@router.get(
    "/segment/{visitorid}",
    response_model=SegmentResponse
)
def customer_segment(visitorid: int):

    result = get_customer_segment(visitorid)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    return result


# --------------------------------------------------
# Existing Customer Recommendation
# --------------------------------------------------

@router.get(
    "/recommend/{visitorid}",
    response_model=RecommendationResponse
)
def recommend(visitorid: int):

    result = get_recommendations(visitorid)

    return result


# --------------------------------------------------
# Popular Recommendations
# --------------------------------------------------

@router.get("/popular")
def popular_items(top_n: int = 10):

    result = get_popular_items(top_n)

    return result
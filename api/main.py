"""
FastAPI Application

Purpose:
Start the RecommendIQ API.
"""

from fastapi import FastAPI

from api.routes import router #type:ignore


# Create FastAPI application
app = FastAPI(
    title="RecommendIQ API",
    description="Smart Recommendation & Personalization Engine",
    version="1.0.0"
)


# Register all API routes
app.include_router(router)
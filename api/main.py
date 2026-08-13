"""
FastAPI Application

Purpose:
Start the RecommendIQ API.
"""

from fastapi import FastAPI

from api.routes import router #type:ignore
from fastapi.middleware.cors import CORSMiddleware 

# Create FastAPI application
app = FastAPI(
    title="RecommendIQ API",
    description="Smart Recommendation & Personalization Engine",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register all API routes
app.include_router(router)
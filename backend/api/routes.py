"""
api/routes.py

Defines the FastAPI routes for the application.
This module contains the `/search` endpoint for querying fashion images using natural language.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services.search import search_images

router = APIRouter()

class SearchRequest(BaseModel):
    """
    Request model for the /search endpoint.

    Attributes:
        query (str): The user's text query (e.g. "red leather jacket").
        top_k (int): Number of top matching images to return (default: 5).
    """
    query: str
    top_k: int = 5


class SearchResponse(BaseModel):
    """
    Response model for the /search endpoint.

    Attributes:
        results (List[str]): List of image URLs matching the query.
    """
    results: List[str]


@router.post("/search", response_model=SearchResponse)
def search_route(payload: SearchRequest):
    """
    Search fashion images based on a text query using the CLIP + FAISS backend.

    Args:
        payload (SearchRequest): Contains the text query and number of results to return.

    Returns:
        SearchResponse: A list of image URLs (served from static directory) ranked by similarity.
    """
    results = search_images(payload.query, payload.top_k)
    return {"results": results}

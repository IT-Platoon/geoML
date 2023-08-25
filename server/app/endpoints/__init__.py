from app.endpoints.search import api_router as search_router


list_of_routes = [
    search_router,
]


__all__ = [
    "list_of_routes",
]

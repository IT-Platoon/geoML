from fastapi import APIRouter, Query, Request, responses, status

api_router = APIRouter(
    prefix="/search",
    tags=["GeoML"],
)

@api_router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def start_page(
    request: Request,
    address: str = Query(default="", alias="address"),
    count: int = Query(default=10, alias="count"),
):
    return {
        "query": address,
        "result" : [
            {"id":1, "address": address},
        ]
        
    }

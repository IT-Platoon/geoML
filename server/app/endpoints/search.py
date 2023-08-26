from fastapi import APIRouter, Query, Request, responses, status

api_router = APIRouter(
    prefix="/search",
    tags=["geo_ml"],
)

@api_router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def search(
    request: Request,
    address: str = Query(default="", alias="address"),
    count: int = Query(default=10, alias="count"),
):
    return {
        "query": address,
        "result" : [
            {"id":1, "address": 'г. Санкт-Петербург, ул. Достоевского, д. 44 литера Е'},
        ] * count
        
    }

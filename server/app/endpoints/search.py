from fastapi import APIRouter, Query, Request, responses, status

def example(count: int = 10):
    return [
        {"id": i+1, "address": f'г. Санкт-Петербург, ул. Достоевского, д. {i+1} литера Е'}
        for i in range(count)
    ]

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
        "result" : example(count)        
    }

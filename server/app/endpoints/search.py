from fastapi import APIRouter, Query, Request, responses, status
from ..desktop.searcher import get_addresses_clean
from ..desktop.constants import MODEL_PATH, RESPONSE_COUNT

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
    count: int = Query(default=RESPONSE_COUNT, alias="count"),
):
    result = get_addresses_clean(address, count)
    print(result)
    
    if result is None:
        return {}
        
    return {
        "query": address,
        "result": result
    }

from fastapi import APIRouter, Query, Request, responses, status
from ..desktop.searcher import find_address
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
    result = find_address(MODEL_PATH, address)
    print(result)
    
    if result is None:
        return {}
        
    return {
        "query": address,
        "result": [
            {"id": i, "address": ''} for i in result['target_building_id']
        ]
    }

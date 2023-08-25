from fastapi import APIRouter, Query, Request, responses, status, templating


api_router = APIRouter(
    prefix="/search",
    tags=["GeoML"],
)
templates = templating.Jinja2Templates(directory="app/templates")


@api_router.get(
    "",
    response_class=responses.HTMLResponse,
    status_code=status.HTTP_200_OK,
)
async def start_page(
    request: Request,
    address: str = Query(default="", alias="address"),
    count: int = Query(default=10, alias="count"),
):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "address": address, "count": count},
    )

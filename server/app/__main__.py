from fastapi import FastAPI, staticfiles
from uvicorn import run

from app.config import DefaultSettings, get_settings
from app.endpoints import list_of_routes
from app.utils.common import get_hostname


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "My new FastAPI project"

    tags_metadata = [
        {
            "name": "geo_ml",
            "description": "My new FastAPI project",
        },
    ]

    application = FastAPI(
        title="app",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi",
        version="0.1.0",
        openapi_tags=tags_metadata,
    )
    settings = get_settings()
    application.mount(
        "/static",
        staticfiles.StaticFiles(directory="app/static"),
        name="static",
    )
    bind_routes(application, settings)
    application.state.settings = settings
    return application


app = get_app()

if __name__ == "__main__":
    settings_for_application = get_settings()
    run(
        "app.__main__:app",
        host=get_hostname(settings_for_application.APP_HOST),
        port=settings_for_application.APP_PORT,
        reload=True,
        reload_dirs=["app", "tests"],
        log_level="debug",
    )

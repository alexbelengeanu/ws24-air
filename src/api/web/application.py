from fastapi import FastAPI
from fastapi.responses import UJSONResponse

import src.api.web.lifetime as lifetime
import src.api.web.router as router


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of the application.

    :return: application.
    """

    app = FastAPI(
        title="Celebrity Clone API",
        description="This is the API for the Celebrity Clone project - WS24 AIR.",
        docs_url=f"/api/v1/docs",
        redoc_url=f"/api/v1/redoc",
        openapi_url=f"/api/v1/openapi.json",
        default_response_class=UJSONResponse,
    )

    lifetime.register_startup_events(app)
    lifetime.register_shutdown_events(app)

    app.include_router(router=router.api_router, prefix=f"/api/v1")

    return app
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from src.api import DatabaseManager, get_manager
from ..lifetime import ImageCollection, get_collection


router = APIRouter(tags=["Check"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    description="Checks the health of a project.",
)
def health_check() -> JSONResponse:
    """
    Checks the health of a project.

    :return: JSONResponse
    """
    return JSONResponse(
        content={"status": "ok"},
    )


@router.get(
    "/dependencies",
    status_code=status.HTTP_200_OK,
    description="Returns the current status of the dependencies that were injected (database manager, image collection and the dataset).",
)
def dependencies(
        db_manager: DatabaseManager = Depends(get_manager),
        img_collection: ImageCollection = Depends(get_collection)
) -> JSONResponse:
    """
    Returns the current status of the injected dependencies.

    :return: JSONResponse
    """
    return JSONResponse(
        content={
            "client_was_set": True if db_manager.get_client() else False,
            "collection_was_set": True if img_collection else False,
        },
    )
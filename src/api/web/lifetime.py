from typing import Awaitable, Callable, Union

from fastapi import FastAPI

from src.storage.collection import ImageCollection
from src.api import db_manager
from .settings import app_settings

img_collection = None

def register_startup_events(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        """
        Actions to run on application startup.

        :return: None
        """
        db_manager.create_client(remove_if_exists=app_settings.remove_if_exists)
        global img_collection
        img_collection = ImageCollection(
            client=db_manager.get_client(),
            dimension=app_settings.embedding_dim,
            metric_type=app_settings.similarity_metric
        )
    return _startup


def register_shutdown_events(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        """
        Actions to run on application's shutdown.

        :return: None
        """
        db_manager.stop_client()

    return _shutdown


def get_collection() -> Union[ImageCollection, None]:
    """
    Get the image collection.

    :return: ImageCollection
    """
    if img_collection is None:
        raise ValueError("Image collection is not initialized.")
    else:
        return img_collection
from typing import Union

from ..storage.client import DatabaseManager
from ..storage.collection import ImageCollection
from ..storage.dataset import Dataset
from .web.settings import app_settings

db_manager = DatabaseManager(db_name=app_settings.db_name)


def get_manager() -> DatabaseManager:
    """
    Get the object_detection.
    """

    return db_manager

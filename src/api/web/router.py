from fastapi.routing import APIRouter
from .views import check_router, db_query_router

api_router = APIRouter()
api_router.include_router(check_router)
api_router.include_router(db_query_router)
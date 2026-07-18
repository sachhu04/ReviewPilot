from fastapi import APIRouter
from api.routes import auth, review

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(review.router, prefix="/review", tags=["review"])

from fastapi import FastAPI, APIRouter

from app.apis.endpoints import auth_router, users_router, opa_router, gold_router
from app.core import get_settings

settings = get_settings()


def init_router(app: FastAPI):
    main_router = APIRouter(prefix=settings.BASE_API_SLUG)

    main_router.include_router(auth_router)
    main_router.include_router(users_router)
    main_router.include_router(opa_router)
    main_router.include_router(gold_router)

    app.include_router(main_router)


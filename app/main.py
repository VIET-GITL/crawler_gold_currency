import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import get_settings
from app.opa import create_opa_bundle
from app.routes import init_router
from app.tasks import celery_app

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_router(app)


@app.on_event("startup")
async def startup_event():
    create_opa_bundle()
    celery_app.conf.update(
        broker_url='redis://localhost:6379/0',
        result_backend='redis://localhost:6379/0',
    )


@app.get("/")
def root():
    return {"successfully": "Welcome to crawler"}




from fastapi import FastAPI
from basic_utils.logger import get_logger
from contextlib import asynccontextmanager
from basic_utils.config import settings
import app.admin as admin_models
from prometheus_fastapi_instrumentator import Instrumentator
from middleware.timing import TimingMiddleware




@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    try:
        ...
    except Exception as e:
        ...
    yield

app = FastAPI(title=settings.app_name,
    description=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(TimingMiddleware)


Instrumentator().instrument(app).expose(app)

@app.get("/")
async def index():
    logger = get_logger("main")
    await logger.info("index called")
    return {"message": "index"}
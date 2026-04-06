from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from basic_utils.logger import get_logger
from contextlib import asynccontextmanager
from basic_utils.config import settings
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)


Instrumentator().instrument(app).expose(app)

@app.get("/")
async def index():
    logger = get_logger("main")
    await logger.info("index called")
    return {"message": "index"}

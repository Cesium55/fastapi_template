from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Базовые настройки приложения"""
    
    # Настройки приложения
    app_name: str = "app"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"
    
    # Настройки сервера
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    
    # Настройки базы данных
    db_sync_driver: str = "postgresql"
    db_async_driver: str = "postgresql+asyncpg"
    db_user: str = "user"
    db_password: str = "password"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "food_link"
    
    # Настройки CORS
    allowed_origins: list[str] = ["*"]
    allowed_methods: list[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allowed_headers: list[str] = ["*"]
    cors_allow_credentials: bool = False
    
    # Настройки логирования
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Настройки Celery
    celery_broker_url: Optional[str] = None
    celery_result_backend: Optional[str] = None
    
    # Настройки Redis
    redis_url: Optional[str] = None
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # Настройки S3/MinIO
    s3_endpoint_url: str = "http://localhost:9000"
    s3_access_key_id: str = "minioadmin"
    s3_secret_access_key: str = "minioadmin"
    s3_bucket_name: str = "food-link-images"
    s3_region_name: str = "us-east-1"

    # Настройки JWT
    jwt_algorithms: list[str] = ["RS256"]
    jwt_audience: Optional[str] = None
    jwt_issuer: Optional[str] = None
    jwt_verify_exp: bool = True
    jwt_public_key: str = ""
    jwt_public_key_url: str = "http://localhost:8000/keys/public"
    jwt_public_key_response_field: str = "public_key"
    jwt_public_key_request_timeout: float = 5.0
    jwt_public_key_cache_prefix: str = "jwt:public_key"
    jwt_public_key_cache_ttl: int = 3600
    jwt_default_key_id: str = "default"

    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "allow"


# Создаем глобальный экземпляр настроек
settings = Settings()

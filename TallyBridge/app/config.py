"""
Application Configuration
Environment variables and settings
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Optional, Union
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Application Starter Kit"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Email Settings Encryption
    EMAIL_SETTINGS_ENCRYPTION_KEY: str = "change-me-email-settings-key"
    
    # Allowed Hosts
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "0.0.0.0", "*"]
    
    # CORS - stored as string, parsed to list
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000,http://localhost:8080,http://localhost:8901,http://127.0.0.1:8901"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse ALLOWED_ORIGINS string to list"""
        if isinstance(self.ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
        return self.ALLOWED_ORIGINS
    
    # Worker Configuration
    WORKERS: int = 1

    # Redis (Queue/Status)
    REDIS_URL: str = "redis://localhost:6379/0"
    EXPORT_JOBS_QUEUE_NAME: str = "export_jobs"
    EMAIL_JOBS_QUEUE_NAME: str = "email_jobs"

    EMAIL_MAX_RETRY_COUNT: int = 5
    EMAIL_RETRY_BACKOFF_SECONDS: str = "30,120,300,900,1800"
    EMAIL_RETRY_SWEEP_INTERVAL_SECONDS: int = 5

    # Export file storage (Local Disk)
    EXPORT_STORAGE_DIR: str = "./export_files"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Password hashing
    PWD_SCHEME: str = "bcrypt"
    PWD_DEPRECATED: str = "auto"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()

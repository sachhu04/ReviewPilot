from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ReviewPilot API"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "postgresql://reviewpilot:password@127.0.0.1:5433/reviewpilot_db"
    
    # JWT
    SECRET_KEY: str = "super-secret-key-change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Groq API
    GROQ_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

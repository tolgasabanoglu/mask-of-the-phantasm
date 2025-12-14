from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # GCP Configuration
    gcp_project_id: Optional[str] = None
    gcp_service_account_key: Optional[str] = None
    
    # API Configuration
    backend_port: int = 8000
    
    # Berlin boundaries [min_lon, min_lat, max_lon, max_lat]
    berlin_bbox: list = [13.0883, 52.3382, 13.7612, 52.6755]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

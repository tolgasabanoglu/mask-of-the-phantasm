import ee
from src.config import settings

class GEEService:
    def __init__(self):
        self.initialized = False
    
    def initialize(self):
        """Initialize Google Earth Engine."""
        try:
            if settings.gcp_service_account_key:
                credentials = ee.ServiceAccountCredentials(
                    settings.gcp_service_account_key
                )
                ee.Initialize(credentials)
            else:
                ee.Initialize()
            
            self.initialized = True
            print("✓ Google Earth Engine initialized")
        except Exception as e:
            print(f"✗ Failed to initialize Google Earth Engine: {e}")
            raise

gee_service = GEEService()

import ee
from typing import Optional
from datetime import datetime

class NightlightService:
    def __init__(self):
        self.dataset_name = "NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG"
    
    def get_nightlight_for_point(
        self,
        lat: float,
        lon: float,
        date_str: str = None
    ) -> Optional[float]:
        """
        Fetch nightlight intensity for a specific point using VIIRS data.
        """
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        target_date = ee.Date(date_str)
        start_date = target_date.advance(-30, 'day')
        
        collection = (
            ee.ImageCollection(self.dataset_name)
            .filterDate(start_date, target_date)
            .filterBounds(ee.Geometry.Point([lon, lat]))
        )
        
        mean_nightlight = collection.select('avg_rad').mean()
        point = ee.Geometry.Point([lon, lat])
        
        try:
            result = mean_nightlight.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point,
                scale=500
            ).getInfo()
            
            return result.get('avg_rad')
        except Exception as e:
            print(f"Error fetching nightlight: {e}")
            return None

nightlight_service = NightlightService()

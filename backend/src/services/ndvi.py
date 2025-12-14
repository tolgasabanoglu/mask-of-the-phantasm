import ee
from typing import List, Optional
from datetime import datetime

class NDVIService:
    def __init__(self):
        self.dataset_name = "COPERNICUS/S2_SR_HARMONIZED"
    
    def get_ndvi_for_point(
        self, 
        lat: float, 
        lon: float, 
        date_str: str = None,
        temporal_window_days: int = 7
    ) -> Optional[float]:
        """
        Fetch NDVI for a specific point using Sentinel-2 data.
        Uses temporal smoothing to mitigate cloud cover.
        """
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        target_date = ee.Date(date_str)
        start_date = target_date.advance(-temporal_window_days, 'day')
        end_date = target_date.advance(temporal_window_days + 1, 'day')
        
        collection = (
            ee.ImageCollection(self.dataset_name)
            .filterDate(start_date, end_date)
            .filterBounds(ee.Geometry.Point([lon, lat]))
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        )
        
        def calc_ndvi(img):
            ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
            return ndvi.copyProperties(img, ['system:time_start'])
        
        ndvi_collection = collection.map(calc_ndvi)
        mean_ndvi = ndvi_collection.mean()
        
        point = ee.Geometry.Point([lon, lat])
        
        try:
            result = mean_ndvi.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point,
                scale=10
            ).getInfo()
            
            return result.get('NDVI')
        except Exception as e:
            print(f"Error fetching NDVI: {e}")
            return None

ndvi_service = NDVIService()

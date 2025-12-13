# Nightcrawler - Dark & Green Routes in Berlin

Generate walking routes through Berlin's darkest and greenest paths using satellite data.

## Overview

Nightcrawler creates circular or polygon-shaped walking routes in Berlin that prioritize two key metrics:

- **Low nightlight values** - Routes through the darkest areas with minimal light pollution
- **High NDVI values** - Routes through areas with dense vegetation and greenery

The application fetches real-time satellite data from Google Cloud Platform to dynamically generate optimal routes based on your preferred distance.

## Features

- Generate circular walking routes of varying distances (2km, 5km, 10km, etc.)
- Choose custom starting point or select Berlin districts/areas
- Real-time nightlight data from VIIRS satellite imagery
- Real-time vegetation data (NDVI) from Sentinel-2 satellite imagery
- Interactive map interface for route visualization

## Technology Stack

### Backend
- FastAPI for REST API
- Google Earth Engine for satellite data
- GeoPandas for geospatial data processing
- NetworkX for graph-based routing algorithms
- OSMnx for OpenStreetMap integration

### Frontend
- React for UI components
- Vite for build tooling
- Mapbox GL JS for interactive maps
- Tailwind CSS for styling

## Project Structure

```
nightcrawler/
├── backend/           # Python FastAPI backend
├── frontend/          # React frontend application
├── data/             # Berlin OSM data and cache
├── docs/             # Documentation
└── scripts/          # Setup and utility scripts
```


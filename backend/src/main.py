from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.services.gee_service import gee_service
from src.api.routes import router

app = FastAPI(
    title="Mask of the Phantasm API",
    description="Generate dark and green walking routes in Berlin",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """Initialize Google Earth Engine on startup."""
    try:
        gee_service.initialize()
    except Exception as e:
        print(f"Warning: Could not initialize GEE: {e}")

@app.get("/")
async def root():
    return {
        "message": "Mask of the Phantasm API is running",
        "version": "0.1.0"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "gee_initialized": gee_service.initialized
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

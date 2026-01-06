from fastapi import FastAPI
import sys
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))
from routes.routes import router


# python -m uvicorn fastapi.main:app --reload --port 8003

app = FastAPI(
    title="USA House Price Prediction",
    description="API de prédiction de prix immobiliers aux USA (R² = 0.76)",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "USA House Price Prediction API",
        "model": "Linear Regression",
        "r2_score": 0.76,
        "features": "13 numeric + one-hot cities",
        "endpoint": "POST /predict/"
    }


@app.get("/health")
async def health():
    try:
        from model_loader import model, scaler
        return {
            "status": "healthy",
            "model_loaded": True,
            "scaler_loaded": True
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@app.get("/cities")
async def get_cities():
    from model_loader import CITIES
    return {
        "count": len(CITIES),
        "cities": sorted(CITIES)
    }

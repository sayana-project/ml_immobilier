from fastapi import APIRouter, HTTPException
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from schemas import HouseFeatures
from predict import Predict


router = APIRouter(prefix="/predict")
predict = Predict()


@router.post("/")
async def predict_price(features: HouseFeatures):
    """
    Prédit le prix d'une maison aux USA.

    Args:
        features: Caractéristiques de la maison

    Returns:
        Prix prédit en USD avec différentes formats
    """
    try:
        prediction = predict.predict_price(features.model_dump())
        return {
            "predicted_price": {
                "usd": round(prediction, 2),
                "k_usd": round(prediction / 1000, 2),
                "m_usd": round(prediction / 1000000, 3)
            },
            "input_features": features.model_dump()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")

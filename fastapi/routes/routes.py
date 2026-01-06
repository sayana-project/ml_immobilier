from fastapi import APIRouter,HTTPException,Query
from app.schemas import InputData
from app.predict import Predict

router = APIRouter(prefix="/predict")
predict = Predict()

@router.post("/",summary="Prediction du prix en fonction des différent paramétres",
           description="En lui donnant la ville exacte qui est dans la liste des villes converte l'endpoint peux prédire un prix")
async def predict_ville(data: InputData, city: str = Query(..., description="Ville cible (lille ou bordeaux)")):
    """
    Renvoie la prédiction du prix au m² en fonction de la ville.
    
    Returns:
        List[Dict[str, Any]]: Liste des parametre du bien immobilié
        
    Raises:
        HTTPException: Si des données manquantes
    """
    city=city.lower()
    try:
        prediction, type_local, model, data_intel = await predict.predict_price(data.model_dump(), city)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {
        "ville": city,  
        "model": model,
        "features":{
            "surface_bati": data_intel["surface_bati"],
            "nombre_pieces": data_intel["nombre_pieces"],
            "type_local": type_local, 
            "surface_terrain": data_intel["surface_terrain"],
            "nombre_lots": data_intel["nombre_lots"],
            "prediction m²": prediction
        },
    }

@router.post("/lille/",summary="Prediction du prix en fonction des différent paramétres sur la ville de lille",
           description="l'endpoint pour prédire un prix sur la ville de lille")
async def predict_lille(data: InputData):
    """
    Renvoie la prédiction du prix au m² sur la ville de lille.
    
    Returns:
        List[Dict[str, Any]]: Liste des parametre du bien immobilié
        
    Raises:
        HTTPException: Si des données manquantes
    """
    prediction,type_local,model, data_intel = await predict.predict_price(data.model_dump(), city="lille")

    return {
        "ville": "lille",  
        "model": model,
        "prediction m²": prediction,
        "surface_bati": data_intel["surface_bati"],
        "nombre_pieces": data_intel["nombre_pieces"],
        "type_local": type_local, 
        "surface_terrain": data_intel["surface_terrain"],
        "nombre_lots": data_intel["nombre_lots"],
    }

@router.post("/bordeaux/",summary="Prediction du prix en fonction des différent paramétres sur la ville de bordeaux",
           description="l'endpoint pour prédire un prix sur la ville de bordeaux")
async def predict_bordeaux(data: InputData):
    """
    Renvoie la prédiction du prix au m² sur la ville de lille.
    
    Returns:
        List[Dict[str, Any]]: Liste des parametre du bien immobilié
        
    Raises:
        HTTPException: Si des données manquantes
    """
    prediction,type_local,model, data_intel = await predict.predict_price(data.model_dump(), city="bordeaux")
    return {
        "ville": "bordeaux",  
        "model": model,
        "prediction m²": prediction,
        "surface_bati": data_intel["surface_bati"],
        "nombre_pieces": data_intel["nombre_pieces"],
        "type_local": type_local, 
        "surface_terrain": data_intel["surface_terrain"],
        "nombre_lots": data_intel["nombre_lots"],
    }
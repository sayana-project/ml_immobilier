from joblib import load
from pathlib import Path


# Charger le scaler et le modèle depuis le dossier ml/
MODEL_DIR = Path(__file__).parent.parent / "ml"

scaler = load(MODEL_DIR / "scaler.joblib")
model = load(MODEL_DIR / "model.joblib")

# Villes présentes dans les données d'entraînement (44 villes)
CITIES = [
    "Algona", "Auburn", "Beaux Arts Village", "Bellevue", "Black Diamond",
    "Bothell", "Burien", "Carnation", "Clyde Hill", "Covington",
    "Des Moines", "Duvall", "Enumclaw", "Fall City", "Federal Way",
    "Inglewood-Finn Hill", "Issaquah", "Kenmore", "Kent", "Kirkland",
    "Lake Forest Park", "Maple Valley", "Medina", "Mercer Island", "Milton",
    "Newcastle", "Normandy Park", "North Bend", "Pacific", "Preston",
    "Ravensdale", "Redmond", "Renton", "Sammamish", "SeaTac", "Seattle",
    "Shoreline", "Skykomish", "Snoqualmie", "Snoqualmie Pass", "Tukwila",
    "Vashon", "Woodinville", "Yarrow Point"
]

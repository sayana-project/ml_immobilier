from joblib import load
from pathlib import Path


# Chargement des modèles et scalers
model_appt = load("models" / "model_regression_apartement.pkl")
scaler_X_appt = load("models" / "scaler_X_apartement.pkl")

model_house = load("models" / "model_regression_house.pkl")
scaler_X_house = load("models" / "scaler_X_house.pkl")
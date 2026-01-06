# app/predict.py
import asyncio
import numpy as np
from app.model_loader import model_appt, scaler_X_appt, model_house, scaler_X_house

class Predict:
    async def predict_price(self, data: dict, city: str):
        city = city.lower()
        if city not in ["lille", "bordeaux"]:
            raise ValueError(f"Ville inconnue : {city} (seules 'lille' et 'bordeaux' sont autorisées)")

        print(f"Données reçues: {data}")
        model = "LinearRegression"
        type_local = data.get("type_local", "").lower()

        required_features = ['surface_bati', 'nombre_pieces', 'nombre_lots']
        missing = [feat for feat in required_features if feat not in data]
        if missing:
            raise ValueError(f"Champ(s) manquant(s) dans la requête : {', '.join(missing)}")

        possible_features = {
            'surface_bati': data["surface_bati"],
            'nombre_pieces': data["nombre_pieces"],
            'nombre_lots': data["nombre_lots"],
            'surface_terrain': data.get("surface_terrain", 0)
        }

        def _predict():
            nonlocal model  # pour modifier la variable model définie dans l'enclos
            if type_local == "maison":
                feature_to_use = ["surface_terrain", "surface_bati"]
                X = np.array([possible_features[feature] for feature in feature_to_use]).reshape(1, -1)
                print(f"Features maison ({feature_to_use}) - Shape: {X.shape}, Valeurs: {X}")
                X_scaled = scaler_X_house.transform(X)
                prediction = model_house.predict(X_scaled)[0]

            elif type_local == "appartement":
                feature_to_use = ["nombre_lots", "surface_bati"]
                X = np.array([possible_features[feature] for feature in feature_to_use]).reshape(1, -1)
                print(f"Features appartement ({feature_to_use}) - Shape: {X.shape}, Valeurs: {X}")
                X_scaled = scaler_X_appt.transform(X)
                prediction = model_appt.predict(X_scaled)[0]
                model = "XGBRegressor"
            else:
                raise ValueError("type_local doit être 'maison' ou 'appartement'")

            return float("{:.2f}".format(prediction)), str(type_local), str(model), data

        try:
            return await asyncio.to_thread(_predict)
        except KeyError as e:
            raise ValueError(f"Clé manquante dans les données : {e}")
        except Exception as e:
            print(f"🔥 Erreur dans predict_price: {str(e)}")
            import traceback
            traceback.print_exc()
            raise ValueError("Erreur interne lors de la prédiction. Vérifiez les champs saisis.")
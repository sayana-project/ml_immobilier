import numpy as np
import pandas as pd
from model_loader import scaler, model, CITIES


class Predict:
    def __init__(self):
        # Colonnes dans l'ordre attendu par le modèle
        self.feature_columns = [
            'year', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot',
            'floors', 'waterfront', 'view', 'condition', 'sqft_basement',
            'yr_built', 'yr_renovated'
        ]
        self.cities = CITIES

    def predict_price(self, features: dict):
        """
        Prédit le prix d'une maison.

        Args:
            features: dict avec les clés year, bedrooms, bathrooms, sqft_living,
                      sqft_lot, floors, waterfront, view, condition, sqft_basement,
                      yr_built, yr_renovated, city

        Returns:
            float: prix prédit (normalisé, entre 0 et 1)
        """
        # Normaliser la ville (insensible à la casse)
        city_input = features.get('city', '')
        city_normalized = city_input.strip().title()

        # Vérifier que la ville est connue
        if city_normalized not in self.cities:
            raise ValueError(f"Ville inconnue: {city_input}. Villes disponibles: {', '.join(sorted(self.cities))}")

        # Créer le DataFrame avec les features numériques
        data = {col: features[col] for col in self.feature_columns}
        df = pd.DataFrame([data])

        # Ajouter les colonnes one-hot pour les villes
        for c in self.cities:
            df[f'city_{c}'] = 1 if c == city_normalized else 0

        # S'assurer que l'ordre des colonnes correspond à celui de l'entraînement
        # L'ordre est: [features numériques] + [city_*]
        df = df[self.feature_columns + [f'city_{c}' for c in self.cities]]

        # Normaliser avec le scaler
        X_scaled = scaler.transform(df)

        # Prédire
        prediction = model.predict(X_scaled)[0]

        return float(prediction)

# USA House Price Prediction API

> API REST pour la prédiction de prix immobiliers aux USA utilisant Machine Learning (Linear Regression)

**Model Performance** : R² = 0.67 | **Tech Stack** : Python, FastAPI, Scikit-Learn

---

## Features

- 🏠 **Prédiction de prix** : Estimation du prix de maisons aux USA
- 🌆 **44 villes supportées** : Seattle, Bellevue, Kirkland, Redmond, etc.
- 🔄 **3 endpoints** : Health check, liste des villes, prédiction
- 📊 **Formats multiples** : Prix en USD, K USD, M USD
- 🔤 **Casse insensible** : `seattle`, `Seattle`, `SEATTLE` fonctionnent tous

---

## Quick Start

### Prérequis

- Python 3.10+
- Virtual environment recommandé

### Installation

```bash
# Cloner le repository
git clone https://github.com/sayana-project/ml_immobilier.git
cd ml_immobilier

# Creer un environnement virtuel
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Installer les dependances
pip install -r requirements.txt
```

### Lancer l'API

```bash
# Development (avec auto-reload)
uvicorn api.main:app --reload --port 8003

# Production
uvicorn api.main:app --port 8003
```

L'API sera accessible sur : **http://localhost:8003**

---

## API Documentation

### Endpoints

#### 1. Health Check

Vérifie que l'API fonctionne et que les modèles sont chargés.

```bash
GET /health
```

**Response :**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "scaler_loaded": true
}
```

---

#### 2. Liste des villes

Retourne la liste des 44 villes supportées.

```bash
GET /cities
```

**Response :**
```json
{
  "count": 44,
  "cities": [
    "Algoma",
    "Auburn",
    "Beaux Arts Village",
    "Bellevue",
    "Black Diamond",
    ...
  ]
}
```

---

#### 3. Prédiction de prix

Prédit le prix d'une maison basé sur ses caractéristiques.

```bash
POST /predict/
Content-Type: application/json
```

**Request Body :**
```json
{
  "year": 2014,
  "bedrooms": 3,
  "bathrooms": 2,
  "sqft_living": 2000,
  "sqft_lot": 8000,
  "floors": 1,
  "waterfront": 0,
  "view": 0,
  "condition": 4,
  "sqft_basement": 500,
  "yr_built": 1990,
  "yr_renovated": 0,
  "city": "seattle"
}
```

**Response :**
```json
{
  "predicted_price": {
    "usd": 639288.45,
    "k_usd": 639.29,
    "m_usd": 0.639
  },
  "input_features": {
    "year": 2014,
    "bedrooms": 3,
    "bathrooms": 2,
    ...
  }
}
```

---

## Features Description

| Feature | Type | Description | Range |
|---------|------|-------------|-------|
| `year` | int | Année de la transaction | 2014 |
| `bedrooms` | int | Nombre de chambres | 0-9 |
| `bathrooms` | int | Nombre de salles de bain | 0-8 |
| `sqft_living` | int | Surface habitable (pi²) | 370-13540 |
| `sqft_lot` | int | Surface du terrain (pi²) | 638-1074218 |
| `floors` | int | Nombre d'étages | 1-3 |
| `waterfront` | int | Vue sur l'eau (0/1) | 0-1 |
| `view` | int | Qualité de la vue (0-4) | 0-4 |
| `condition` | int | État général (1-5) | 1-5 |
| `sqft_basement` | int | Surface du sous-sol (pi²) | 0-4820 |
| `yr_built` | int | Année de construction | 1900-2014 |
| `yr_renovated` | int | Année de rénovation (0 = jamais) | 0-2014 |
| `city` | string | Ville (insensible à la casse) | 44 villes |

---

## Model Details

### Algorithm

- **Type** : Linear Regression
- **Features** : 13 numériques + One-Hot Encoding pour 44 villes (57 total)
- **Scaling** : MinMaxScaler (0-1)
- **R² Score** : 0.67
- **Dataset** : 4,551 maisons dans l'État de Washington (USA)

### Training

```python
# Separe features et target
y = house["price"]
x = house.drop("price", axis=1)

# Normalisation
scaler = MinMaxScaler(feature_range=(0, 1))
x_scaled = scaler.fit_transform(x)

# Entrainement
model = LinearRegression()
model.fit(X_train, Y_train)
```

---

## Project Structure

```
ml_immobilier/
├── api/                        # FastAPI application
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── model_loader.py         # Charge modele et scaler
│   ├── predict.py              # Logique de prediction
│   ├── schemas.py              # Pydantic models
│   └── routes/
│       ├── __init__.py
│       └── routes.py           # API endpoints
├── ml/                         # Machine Learning
│   ├── data/                   # Dataset
│   │   └── data.csv
│   ├── model.joblib            # Modele entraine
│   ├── scaler.joblib           # Scaler
│   └── house-price-prediction-linear-regression.ipynb  # Notebook
├── requirements.txt             # Dependances Python
└── README.md                   # Ce fichier
```

---

## Example Usage

### cURL

```bash
curl -X POST 'http://localhost:8003/predict/' \
  -H 'Content-Type: application/json' \
  -d '{
  "year": 2014,
  "bedrooms": 3,
  "bathrooms": 2,
  "sqft_living": 2000,
  "sqft_lot": 8000,
  "floors": 1,
  "waterfront": 0,
  "view": 0,
  "condition": 4,
  "sqft_basement": 500,
  "yr_built": 1990,
  "yr_renovated": 0,
  "city": "seattle"
}'
```

### Python

```python
import requests

response = requests.post(
    "http://localhost:8003/predict/",
    json={
        "year": 2014,
        "bedrooms": 3,
        "bathrooms": 2,
        "sqft_living": 2000,
        "sqft_lot": 8000,
        "floors": 1,
        "waterfront": 0,
        "view": 0,
        "condition": 4,
        "sqft_basement": 500,
        "yr_built": 1990,
        "yr_renovated": 0,
        "city": "seattle"
    }
)

price = response.json()["predicted_price"]["usd"]
print(f"Predicted price: ${price:,.2f}")
```

---

## Development

### Lancer en mode dev

```bash
uvicorn api.main:app --reload --port 8003
```

### Documentation interactive

Ouvrez votre navigateur sur : **http://localhost:8003/docs**

Swagger UI fournit une documentation interactive complète de l'API.

---

## License

MIT License

---

**Author** : Sayana Project
**Repository** : [https://github.com/sayana-project/ml_immobilier](https://github.com/sayana-project/ml_immobilier)

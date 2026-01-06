from pydantic import BaseModel
from typing import Optional


class HouseFeatures(BaseModel):
    year: int
    bedrooms: int
    bathrooms: int
    sqft_living: int
    sqft_lot: int
    floors: int
    waterfront: int
    view: int
    condition: int
    sqft_basement: int
    yr_built: int
    yr_renovated: int
    city: str

from pydantic import BaseModel
from typing import Optional

class InputData(BaseModel):
    surface_bati: float
    nombre_pieces: int
    type_local: str  # "maison" ou "appartement"
    surface_terrain: Optional[float] = None  # facultatif
    nombre_lots: int
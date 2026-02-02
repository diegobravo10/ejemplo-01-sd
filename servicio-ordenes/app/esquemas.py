from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

class OrdenCrear(BaseModel):
    producto_id: int = Field(gt=0)
    cantidad: int = Field(gt=0)

class OrdenRespuesta(BaseModel):
    id: int
    producto_id: int
    producto_nombre: str
    precio_unitario: Decimal
    cantidad: int
    total: Decimal
    estado: str
    creada_en: datetime | None

    class Config:
        from_attributes = True

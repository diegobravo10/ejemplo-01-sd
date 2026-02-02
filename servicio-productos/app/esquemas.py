from pydantic import BaseModel, Field
from decimal import Decimal

class ProductoCrear(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    precio: Decimal = Field(gt=0)
    stock: int = Field(ge=0)

class ProductoRespuesta(BaseModel):
    id: int
    nombre: str
    precio: Decimal
    stock: int

    class Config:
        from_attributes = True

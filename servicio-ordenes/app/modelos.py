from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from .db import Base

class Orden(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True, index=True)

    producto_id = Column(Integer, nullable=False)
    producto_nombre = Column(String(120), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)

    cantidad = Column(Integer, nullable=False)
    total = Column(Numeric(10, 2), nullable=False)

    estado = Column(String(30), nullable=False, default="CREADA")
    creada_en = Column(DateTime(timezone=True), server_default=func.now())

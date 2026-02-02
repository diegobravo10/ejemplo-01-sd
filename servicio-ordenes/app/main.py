import os
import httpx
from decimal import Decimal

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select

from .db import Base, engine, SessionLocal
from .modelos import Orden
from .esquemas import OrdenCrear, OrdenRespuesta

PRODUCTOS_URL = os.getenv("PRODUCTOS_URL", "http://localhost:8000")

app = FastAPI(title="Servicio de Órdenes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/ordenes", response_model=OrdenRespuesta)
async def crear_orden(payload: OrdenCrear, db: Session = Depends(get_db)):
    # 1) Obtener producto
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{PRODUCTOS_URL}/productos/{payload.producto_id}")
        if r.status_code == 404:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        if r.status_code >= 400:
            raise HTTPException(status_code=502, detail="Error consultando servicio de productos")
        producto = r.json()

    # 2) Descontar stock
    async with httpx.AsyncClient(timeout=10) as client:
        r2 = await client.patch(
            f"{PRODUCTOS_URL}/productos/{payload.producto_id}/descontar-stock",
            params={"cantidad": payload.cantidad},
        )
        if r2.status_code == 409:
            raise HTTPException(status_code=409, detail="Stock insuficiente")
        if r2.status_code >= 400:
            raise HTTPException(status_code=502, detail="No se pudo descontar stock")

    precio = Decimal(str(producto["precio"]))
    total = precio * payload.cantidad

    o = Orden(
        producto_id=payload.producto_id,
        producto_nombre=producto["nombre"],
        precio_unitario=precio,
        cantidad=payload.cantidad,
        total=total,
        estado="CREADA",
    )
    db.add(o)
    db.commit()
    db.refresh(o)
    return o

@app.get("/ordenes", response_model=list[OrdenRespuesta])
def listar_ordenes(db: Session = Depends(get_db)):
    rows = db.execute(select(Orden).order_by(Orden.id.desc())).scalars().all()
    return rows

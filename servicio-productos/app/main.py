from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select

from .db import Base, engine, SessionLocal
from .modelos import Producto
from .esquemas import ProductoCrear, ProductoRespuesta

app = FastAPI(title="Servicio de Productos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # para demo
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

@app.post("/productos", response_model=ProductoRespuesta)
def crear_producto(payload: ProductoCrear, db: Session = Depends(get_db)):
    p = Producto(nombre=payload.nombre, precio=payload.precio, stock=payload.stock)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@app.get("/productos", response_model=list[ProductoRespuesta])
def listar_productos(db: Session = Depends(get_db)):
    rows = db.execute(select(Producto).order_by(Producto.id.desc())).scalars().all()
    return rows

@app.get("/productos/{producto_id}", response_model=ProductoRespuesta)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    p = db.get(Producto, producto_id)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p

@app.patch("/productos/{producto_id}/descontar-stock", response_model=ProductoRespuesta)
def descontar_stock(producto_id: int, cantidad: int, db: Session = Depends(get_db)):
    if cantidad <= 0:
        raise HTTPException(status_code=400, detail="cantidad debe ser > 0")
    p = db.get(Producto, producto_id)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if p.stock < cantidad:
        raise HTTPException(status_code=409, detail="Stock insuficiente")
    p.stock -= cantidad
    db.commit()
    db.refresh(p)
    return p

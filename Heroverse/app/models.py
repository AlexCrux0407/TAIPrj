from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
import datetime

from .database import Base

class Comic(Base):
    __tablename__ = "comics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    image_url = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    telefono = Column(String)
    direccion = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, index=True)
    telefono = Column(String)
    direccion = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
    estado = Column(String, default="pendiente")
    total = Column(Float, default=0.0)
    
    # Relación con el cliente
    cliente = relationship("Cliente", back_populates="pedidos")
    # Relación con los detalles del pedido
    detalles = relationship("DetallePedido", back_populates="pedido")

# Añadimos la relación en la clase Cliente
Cliente.pedidos = relationship("Pedido", back_populates="cliente")

class DetallePedido(Base):
    __tablename__ = "detalles_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    comic_id = Column(Integer, ForeignKey("comics.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    
    # Relaciones
    pedido = relationship("Pedido", back_populates="detalles")
    comic = relationship("Comic")
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

# Datos iniciales para cómics 
def init_db(db):
    # Verificar si ya hay cómics en la base de datos
    comics_count = db.query(Comic).count()
    if comics_count == 0:
        comics_data = [
            {"title": "Dragon Ball Super Vol. 1", "image_url": "/static/images/comic.png", "price": 50.8, "stock": 52},
            {"title": "Dragon Ball Super Vol. 2", "image_url": "/static/images/comic.png", "price": 50.8, "stock": 52},
            {"title": "Dragon Ball Super Vol. 3", "image_url": "/static/images/comic.png", "price": 50.8, "stock": 52},
            {"title": "Dragon Ball Super Vol. 4", "image_url": "/static/images/comic.png", "price": 50.8, "stock": 52},
            {"title": "Dragon Ball Super Vol. 5", "image_url": "/static/images/comic.png", "price": 50.8, "stock": 52},
            {"title": "Dragon Ball Super Vol. 6", "image_url": "/static/images/comic.png", "price": 50.8, "stock": 52},
            {"title": "Dragon Ball Super Vol. 7", "image_url": "/static/images/comic.png", "price": 50.8, "stock": 52},
            {"title": "Dragon Ball Super Vol. 8", "image_url": "/static/images/comic.png", "price": 50.8, "stock": 52},
        ]
        
        for comic_data in comics_data:
            comic = Comic(**comic_data)
            db.add(comic)
        
        db.commit()
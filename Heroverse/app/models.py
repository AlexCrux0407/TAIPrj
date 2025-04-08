from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class Comic(Base):
    __tablename__ = "comics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    image_url = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    limite_minimo = Column(Integer, nullable=True, default=10)  


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    telefono = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Campos adicionales para clientes frecuentes
    fecha_nacimiento = Column(DateTime, nullable=True)
    nivel = Column(String, nullable=True, default="bronze")
    puntos = Column(Integer, nullable=True, default=0)
    notas = Column(String, nullable=True)
    newsletter = Column(Boolean, nullable=True, default=False)
    promociones = Column(Boolean, nullable=True, default=False)
    generos_interes = Column(String, nullable=True)  # Guardar como string separado por comas
    
    # Relación con pedidos
    pedidos = relationship("Pedido", back_populates="cliente")
    
    cambios_nivel = relationship("CambioNivel", back_populates="cliente")



class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, index=True)
    telefono = Column(String)
    direccion = Column(String)
    contacto_nombre = Column(String, nullable=True) 
    contacto_telefono = Column(String, nullable=True)  
    notas = Column(String, nullable=True)  
    created_at = Column(DateTime, default=datetime.utcnow)

    pedidos_proveedor = relationship("PedidoProveedor", back_populates="proveedor")

class PedidoProveedor(Base):
    __tablename__ = "pedidos_proveedor"

    id = Column(Integer, primary_key=True, index=True)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))
    fecha_pedido = Column(DateTime, default=datetime.utcnow)
    fecha_entrega_esperada = Column(DateTime, nullable=True)
    estado = Column(String, default="pending")
    total = Column(Float, default=0.0)
    notas = Column(String, nullable=True)

    # Relaciones
    proveedor = relationship("Proveedor", back_populates="pedidos_proveedor")
    detalles = relationship("DetallePedidoProveedor", back_populates="pedido")

class DetallePedidoProveedor(Base):
    __tablename__ = "detalles_pedidos_proveedor"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos_proveedor.id"))
    comic_id = Column(Integer, ForeignKey("comics.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    subtotal = Column(Float)

    # Relaciones
    pedido = relationship("PedidoProveedor", back_populates="detalles")
    comic = relationship("Comic")

# Update the Proveedor model to include the relationship
Proveedor.pedidos_proveedor = relationship("PedidoProveedor", back_populates="proveedor")

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    fecha = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, default="pendiente")
    total = Column(Float, default=0.0)
    
    # Relación con el cliente
    cliente = relationship("Cliente", back_populates="pedidos")
    # Relación con los detalles del pedido
    detalles = relationship("DetallePedido", back_populates="pedido")

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

class MovimientoStock(Base):
    __tablename__ = "movimientos_stock"

    id = Column(Integer, primary_key=True, index=True)
    comic_id = Column(Integer, ForeignKey("comics.id"))
    cantidad = Column(Integer)
    tipo = Column(String)  # 'entrada' o 'salida'
    razon = Column(String, nullable=True)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    comic = relationship("Comic")
    proveedor = relationship("Proveedor")  # Remove 'nullable=True'


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
        
        
class CambioNivel(Base):
    __tablename__ = "cambios_nivel"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    nivel_anterior = Column(String)
    nivel_nuevo = Column(String)
    motivo = Column(String)
    comentarios = Column(String, nullable=True)
    fecha = Column(DateTime, default=datetime.now(timezone.utc))  
    
    cliente = relationship("Cliente", back_populates="cambios_nivel")
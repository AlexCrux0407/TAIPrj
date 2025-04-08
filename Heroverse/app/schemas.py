from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union
from datetime import datetime

# Esquemas para Comic
class ComicBase(BaseModel):
    title: str
    image_url: str
    price: float
    stock: int = 0
    limite_minimo: Optional[int] = 10  # Add this line

class ComicCreate(ComicBase):
    min_stock: Optional[int] = 5
    max_stock: Optional[int] = 20
    category_id: Optional[int] = None
    isbn: Optional[str] = None

class ComicUpdate(BaseModel):
    title: Optional[str] = None
    image_url: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    limite_minimo: Optional[int] = None  # Add this line
    min_stock: Optional[int] = None
    max_stock: Optional[int] = None
    category_id: Optional[int] = None

class Comic(ComicBase):
    id: int
    min_stock: int = 5
    max_stock: int = 20
    category_id: Optional[int] = None
    isbn: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    category: Optional["Category"] = None
    limite_minimo: Optional[int] = 10  
    
    class Config:
        from_attributes = True

# Esquemas para categorías
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

# Esquemas para Cliente
class ClienteBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    is_frequent: Optional[bool] = None
    loyalty_level: Optional[str] = None
    loyalty_points: Optional[int] = None

class Cliente(ClienteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ClienteFrecuente(ClienteBase):
    id: int
    is_frequent: bool = False
    loyalty_level: Optional[str] = None
    loyalty_points: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True

# Esquemas para Proveedor
class ProveedorBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ProveedorCreate(ProveedorBase):
    contacto_nombre: Optional[str] = None
    contacto_telefono: Optional[str] = None
    notas: Optional[str] = None

class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    contacto_nombre: Optional[str] = None
    contacto_telefono: Optional[str] = None
    notas: Optional[str] = None

class Proveedor(ProveedorBase):
    id: int
    created_at: datetime
    contacto_nombre: Optional[str] = None
    contacto_telefono: Optional[str] = None
    notas: Optional[str] = None

    class Config:
        from_attributes = True

# Esquemas para DetallePedido
class DetallePedidoBase(BaseModel):
    comic_id: int
    cantidad: int
    precio_unitario: Optional[float] = None
    subtotal: Optional[float] = None

class DetallePedidoCreate(DetallePedidoBase):
    pass

class DetallePedidoUpdate(BaseModel):
    cantidad: Optional[int] = None
    precio_unitario: Optional[float] = None
    
class DetallePedido(DetallePedidoBase):
    id: int
    pedido_id: int
    precio_unitario: float
    subtotal: float = 0.0

    class Config:
        from_attributes = True

# Esquemas para Pedido
class PedidoBase(BaseModel):
    cliente_id: Optional[int] = None
    estado: str = "pendiente"
    total: Optional[float] = 0.0

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(BaseModel):
    estado: Optional[str] = None

class Pedido(PedidoBase):
    id: int
    fecha: datetime
    cliente_id: int
    total: float
    detalles: List[DetallePedido] = []

    class Config:
        from_attributes = True

# Esquema extendido para Cliente con sus pedidos
class ClienteConPedidos(Cliente):
    pedidos: List[Pedido] = []

    class Config:
        from_attributes = True

# Esquemas para detalles de pedido a proveedores
class DetallePedidoProveedorBase(BaseModel):
    comic_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float

class DetallePedidoProveedorCreate(DetallePedidoProveedorBase):
    pass

class DetallePedidoProveedor(DetallePedidoProveedorBase):
    id: int
    pedido_id: int
    
    class Config:
        from_attributes = True

# Esquemas para pedidos a proveedores
class PedidoProveedorBase(BaseModel):
    proveedor_id: int
    estado: str = "pending"
    total: float
    notas: Optional[str] = None
    fecha_entrega_esperada: Optional[datetime] = None

class PedidoProveedorCreate(PedidoProveedorBase):
    detalles: List[DetallePedidoProveedorCreate]

class PedidoProveedorUpdate(BaseModel):
    estado: Optional[str] = None
    notas: Optional[str] = None
    fecha_entrega_esperada: Optional[datetime] = None
    fecha_entrega_real: Optional[datetime] = None

class PedidoProveedor(PedidoProveedorBase):
    id: int
    fecha_pedido: datetime
    fecha_entrega_real: Optional[datetime] = None
    detalles: List[DetallePedidoProveedor] = []
    
    class Config:
        from_attributes = True

# Esquemas para promociones
class PromocionBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    descuento: float
    tipo_descuento: str = "porcentaje"
    fecha_inicio: datetime
    fecha_fin: datetime
    niveles_elegibles: str = "all"
    codigo_promocional: Optional[str] = None
    estado: str = "active"

class PromocionCreate(PromocionBase):
    pass

class PromocionUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    descuento: Optional[float] = None
    tipo_descuento: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    niveles_elegibles: Optional[str] = None
    codigo_promocional: Optional[str] = None
    estado: Optional[str] = None

class Promocion(PromocionBase):
    id: int
    
    class Config:
        from_attributes = True

# Esquemas para relación cliente-promoción
class ClientePromocionBase(BaseModel):
    cliente_id: int
    promocion_id: int

class ClientePromocionCreate(ClientePromocionBase):
    pass

class ClientePromocion(ClientePromocionBase):
    id: int
    fecha_envio: datetime
    fecha_uso: Optional[datetime] = None
    usado: bool = False
    
    class Config:
        from_attributes = True

# Esquemas para campañas
class CampanaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    fecha_inicio: datetime
    fecha_fin: datetime
    audiencia: str
    estado: str = "draft"

class CampanaCreate(CampanaBase):
    pass

class CampanaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    audiencia: Optional[str] = None
    estado: Optional[str] = None
    progreso: Optional[int] = None

class Campana(CampanaBase):
    id: int
    progreso: int = 0
    
    class Config:
        from_attributes = True
        
        # Esquema extendido para Cliente con sus pedidos
class ClienteConPedidos(Cliente):
    pedidos: List[Pedido] = []

    class Config:
        from_attributes = True

# Esquemas para MovimientoStock
class MovimientoStockBase(BaseModel):
    comic_id: int
    cantidad: int
    tipo: str
    razon: Optional[str] = None
    proveedor_id: Optional[int] = None

class MovimientoStockCreate(MovimientoStockBase):
    pass

class MovimientoStock(MovimientoStockBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True
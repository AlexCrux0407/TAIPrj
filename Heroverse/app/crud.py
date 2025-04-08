from sqlalchemy.orm import Session
from . import models, schemas

# Funciones CRUD para comics -------------------------------------------------------------------------------------------------------------
def get_comics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comic).offset(skip).limit(limit).all()

def get_comic(db: Session, comic_id: int):
    return db.query(models.Comic).filter(models.Comic.id == comic_id).first()

def create_comic(db: Session, comic: schemas.ComicCreate):
    db_comic = models.Comic(**comic.dict())
    db.add(db_comic)
    db.commit()
    db.refresh(db_comic)
    return db_comic

def update_comic(db: Session, comic_id: int, comic_data: schemas.ComicUpdate):
    db_comic = get_comic(db, comic_id)
    if db_comic:
        for key, value in comic_data.dict(exclude_unset=True).items():
            setattr(db_comic, key, value)
        db.commit()
        db.refresh(db_comic)
    return db_comic

def delete_comic(db: Session, comic_id: int):
    db_comic = get_comic(db, comic_id)
    if db_comic:
        db.delete(db_comic)
        db.commit()
        return True
    return False

# Funciones CRUD para clientes -------------------------------------------------------------------------------------------------------------
def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

def get_cliente(db: Session, cliente_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente
def update_cliente(db: Session, cliente_id: int, cliente_data: schemas.ClienteUpdate):
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        # Actualizar solo los campos proporcionados
        for key, value in cliente_data.dict(exclude_unset=True).items():
            setattr(db_cliente, key, value)
        db.commit()
        db.refresh(db_cliente)
    return db_cliente
def delete_cliente(db: Session, cliente_id: int):
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
        return True
    return False
# Funciones CRUD para proveedores-------------------------------------------------------------------------------------------------------------
def get_proveedores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Proveedor).offset(skip).limit(limit).all()

def get_proveedor(db: Session, proveedor_id: int):
    return db.query(models.Proveedor).filter(models.Proveedor.id == proveedor_id).first()

def create_proveedor(db: Session, proveedor: schemas.ProveedorCreate):
    db_proveedor = models.Proveedor(**proveedor.dict())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor
def update_proveedor(db: Session, proveedor_id: int, proveedor_data: schemas.ProveedorUpdate):
    db_proveedor = get_proveedor(db, proveedor_id)
    if db_proveedor:
        # Actualizar solo los campos proporcionados
        for key, value in proveedor_data.dict(exclude_unset=True).items():
            setattr(db_proveedor, key, value)
        db.commit()
        db.refresh(db_proveedor)
    return db_proveedor

def delete_proveedor(db: Session, proveedor_id: int):
    db_proveedor = get_proveedor(db, proveedor_id)
    if db_proveedor:
        db.delete(db_proveedor)
        db.commit()
        return True
    return False


# Funciones CRUD para pedidos ------------------------------------------------------------------------------------------------------------
def get_pedidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pedido).offset(skip).limit(limit).all()

def get_pedido(db: Session, pedido_id: int):
    return db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()

def create_pedido(db: Session, pedido: schemas.PedidoCreate, cliente_id: int):
    pedido_dict = pedido.dict()
    if 'cliente_id' in pedido_dict:
        del pedido_dict['cliente_id']
    
    db_pedido = models.Pedido(**pedido_dict, cliente_id=cliente_id)
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido
def update_pedido(db: Session, pedido_id: int, pedido_data: schemas.PedidoUpdate):
    db_pedido = get_pedido(db, pedido_id)
    if db_pedido:
        for key, value in pedido_data.dict(exclude_unset=True).items():
            setattr(db_pedido, key, value)
        db.commit()
        db.refresh(db_pedido)
    return db_pedido
def update_detalle_pedido(db: Session, detalle_id: int, detalle_data: schemas.DetallePedidoUpdate):
    db_detalle = db.query(models.DetallePedido).filter(models.DetallePedido.id == detalle_id).first()
    if db_detalle:
        cantidad_antigua = db_detalle.cantidad
        precio_unitario = db_detalle.precio_unitario
        
        for key, value in detalle_data.dict(exclude_unset=True).items():
            setattr(db_detalle, key, value)
        
        if 'cantidad' in detalle_data.dict(exclude_unset=True):
            pedido = get_pedido(db, db_detalle.pedido_id)
            if pedido:
                pedido.total = pedido.total - (cantidad_antigua * precio_unitario) + (db_detalle.cantidad * precio_unitario)
        
        db.commit()
        db.refresh(db_detalle)
    return db_detalle
def delete_pedido(db: Session, pedido_id: int):
    db_pedido = get_pedido(db, pedido_id)
    if db_pedido:
        db.delete(db_pedido)
        db.commit()
        return True
    return False


def add_detalle_pedido(db: Session, detalle: schemas.DetallePedidoCreate, pedido_id: int):
    comic = get_comic(db, detalle.comic_id)
    if not comic:
        return None
    
    db_detalle = models.DetallePedido(
        pedido_id=pedido_id,
        comic_id=detalle.comic_id,
        cantidad=detalle.cantidad,
        precio_unitario=comic.price
    )
    db.add(db_detalle)
    
    comic.stock -= detalle.cantidad
    
    pedido = get_pedido(db, pedido_id)
    pedido.total += comic.price * detalle.cantidad
    
    db.commit()
    db.refresh(db_detalle)
    return db_detalle

def establecer_limite_stock(db: Session, comic_id: int, limite_minimo: int):
    """
    Establecer el límite mínimo de stock para un cómic
    :param db: Sesión de base de datos
    :param comic_id: ID del cómic
    :param limite_minimo: Nuevo límite mínimo de stock
    :return: Cómic actualizado o None si no se encuentra
    """
    try:
        if limite_minimo < 0:
            raise ValueError("El límite mínimo no puede ser negativo")
        
        comic = get_comic(db, comic_id)
        if not comic:
            return None
        
        comic.limite_minimo = min(limite_minimo, comic.stock)
        
        db.commit()
        db.refresh(comic)
        return comic
    except Exception as e:
        db.rollback()
        print(f"Error al establecer límite de stock: {e}")
        raise
# app/crud.py
from sqlalchemy.orm import Session
from datetime import datetime
from .models import Factura, HistorialEstado, EstadoFactura

def crear_factura(db: Session, datos: dict) -> Factura:
    factura = Factura(
        proveedor=datos["proveedor"],
        numero=datos["numero"],
        fecha_emision=datos["fecha_emision"],
        monto_total=datos["monto_total"],
        impuestos=datos.get("impuestos", 0.0),
        fecha_vencimiento=datos.get("fecha_vencimiento"),
        estado=EstadoFactura.EN_PROCESO,
        comentario=None,
        ocr_fuente="imagen",
        ocr_confianza=datos.get("ocr_confianza"),
        creado_en=datetime.utcnow(),
        actualizado_en=datetime.utcnow(),
    )
    db.add(factura)
    db.commit()
    db.refresh(factura)

    historial = HistorialEstado(
        factura_id=factura.id,
        estado=factura.estado.value,
        comentario="Factura creada",
    )
    db.add(historial)
    db.commit()
    return factura

def obtener_factura(db: Session, factura_id: int) -> Factura | None:
    return db.query(Factura).filter(Factura.id == factura_id).first()

def listar_facturas(db: Session) -> list[Factura]:
    return db.query(Factura).order_by(Factura.creado_en.desc()).all()

def actualizar_estado(db: Session, factura: Factura, nuevo_estado: str, comentario: str | None):
    from .models import EstadoFactura
    factura.estado = EstadoFactura(nuevo_estado)
    factura.comentario = comentario
    factura.actualizado_en = datetime.utcnow()

    historial = HistorialEstado(
        factura_id=factura.id,
        estado=nuevo_estado,
        comentario=comentario,
    )
    db.add(historial)
    db.add(factura)
    db.commit()
    db.refresh(factura)
    return factura

def borrar_factura(db: Session, factura_id: int) -> bool:
    from .models import Factura
    factura = db.query(Factura).filter(Factura.id == factura_id).first()
    if not factura:
        return False
    db.delete(factura)
    db.commit()
    return True
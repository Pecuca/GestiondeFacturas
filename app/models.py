from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class EstadoFactura(enum.Enum):
    EN_PROCESO = "En Proceso"
    APROBADO = "Aprobado"
    RECHAZADO = "Rechazado"

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    proveedor = Column(String(255), nullable=False)
    numero = Column(String(100), nullable=False, index=True)
    fecha_emision = Column(DateTime, nullable=False)
    monto_total = Column(Float, nullable=False)
    impuestos = Column(Float, nullable=True, default=0.0)
    fecha_vencimiento = Column(DateTime, nullable=True)

    estado = Column(Enum(EstadoFactura), default=EstadoFactura.EN_PROCESO, nullable=False)
    comentario = Column(Text, nullable=True)

    ocr_fuente = Column(String(50), nullable=True)     # 'imagen' | 'pdf' (usaremos 'imagen')
    ocr_confianza = Column(Float, nullable=True)        # placeholder
    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow)

    historial = relationship("HistorialEstado", back_populates="factura", cascade="all, delete-orphan")

class HistorialEstado(Base):
    __tablename__ = "historial_estados"

    id = Column(Integer, primary_key=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), index=True, nullable=False)
    estado = Column(String(50), nullable=False)
    comentario = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    factura = relationship("Factura", back_populates="historial")
# app/workflows.py
from .models import Factura

def transicionar_estado(factura: Factura, nuevo_estado: str, comentario: str | None):
    # Aquí podrías poner reglas de negocio (ej. no pasar de Rechazado a Aprobado sin re-proceso).
    # Por ahora permitimos cualquier transición válida.
    return factura, {"ok": True}
# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class DecisionInput(BaseModel):
    estado: str       # "Aprobado" | "Rechazado"
    comentario: Optional[str] = None

class NotificacionInput(BaseModel):
    destinatario_email: EmailStr
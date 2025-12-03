# app/notifications.py
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

SMTP_HOST = "smtp.gmail.com"         # Cambia según tu proveedor
SMTP_PORT = 587
SMTP_USER = "tu_correo@gmail.com"    # Configura variables de entorno en producción
SMTP_PASS = "tu_password_app"        # Usa contraseña de aplicación (Gmail)

def enviar_notificacion(destinatario: str, asunto: str, html_contenido: str):
    msg = MIMEText(html_contenido, "html", "utf-8")
    msg["Subject"] = asunto
    msg["From"] = formataddr(("Sistema de Facturas", SMTP_USER))
    msg["To"] = destinatario

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

def plantilla_factura(factura) -> str:
    aprobar_url = f"http://127.0.0.1:8000/facturas/{factura.id}/decision?estado=Aprobado"
    rechazar_url = f"http://127.0.0.1:8000/facturas/{factura.id}/rechazo"

    return f"""
    <div style="font-family: Arial; max-width: 600px; margin:auto;">
      <h2>Factura #{factura.numero}</h2>
      <table style="width:100%; border-collapse: collapse;">
        <tr><th style="text-align:left; border-bottom:1px solid #ddd;">Proveedor</th><td style="border-bottom:1px solid #ddd;">{factura.proveedor}</td></tr>
        <tr><th style="text-align:left; border-bottom:1px solid #ddd;">Monto</th><td style="border-bottom:1px solid #ddd;">{factura.monto_total}</td></tr>
        <tr><th style="text-align:left; border-bottom:1px solid #ddd;">Impuestos</th><td style="border-bottom:1px solid #ddd;">{factura.impuestos}</td></tr>
        <tr><th style="text-align:left; border-bottom:1px solid #ddd;">Estado</th><td style="border-bottom:1px solid #ddd;">{factura.estado.value}</td></tr>
      </table>
      <p>Decisión rápida:</p>
      <a href="{aprobar_url}" style="padding:10px 16px; background:#27ae60; color:#fff; text-decoration:none; border-radius:4px; margin-right:8px;">Aprobar</a>
      <a href="{rechazar_url}" style="padding:10px 16px; background:#e74c3c; color:#fff; text-decoration:none; border-radius:4px;">Rechazar</a>
    </div>
    """
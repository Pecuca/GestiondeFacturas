# app/ocr.py
import pytesseract
from PIL import Image
import re
import tempfile
import datetime

def _parse_date(texto: str):
    m = re.search(r"(\d{2}/\d{2}/\d{4})", texto)
    if not m:
        return None
    try:
        return datetime.datetime.strptime(m.group(1), "%d/%m/%Y")
    except:
        return None

async def extraer_texto(file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    if file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        texto = pytesseract.image_to_string(Image.open(tmp_path))
    else:
        raise ValueError("Solo se permiten imágenes (PNG, JPG, JPEG).")
    return texto

def procesar_campos(texto):
    proveedor = re.search(r"(Proveedor|Supplier)[:\s]+([A-Za-zÁÉÍÓÚÑáéíóúñ\s&.-]+)", texto)
    numero = re.search(r"(Factura|Invoice|No\.|Nro\.|Número)[:\s]+([A-Za-z0-9-]+)", texto)
    fecha = _parse_date(texto)
    monto = re.search(r"(Monto|Total|Amount)[:\s]+\$?([\d.,]+)", texto)
    impuestos = re.search(r"(Impuestos|IVA|Tax)[:\s]+\$?([\d.,]+)", texto)
    venc = re.search(r"(Vencimiento|Due Date)[:\s]+(\d{2}/\d{2}/\d{4})", texto)

    if not (proveedor and numero and fecha and monto):
        return None

    def to_float(s): return float(str(s).replace(".", "").replace(",", ".")) if s else 0.0

    return {
        "proveedor": proveedor.group(2).strip(),
        "numero": numero.group(2).strip(),
        "fecha_emision": fecha,
        "monto_total": to_float(monto.group(2)),
        "impuestos": to_float(impuestos.group(2)) if impuestos else 0.0,
        "fecha_vencimiento": datetime.datetime.strptime(venc.group(2), "%d/%m/%Y") if venc else None,
        "ocr_confianza": None
    }
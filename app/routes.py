# app/routes.py
from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Query, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import database, crud, ocr, schemas
from .notifications import enviar_notificacion, plantilla_factura
from .workflows import transicionar_estado
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.post("/facturas/{factura_id}/borrar")
def borrar_factura(request: Request, factura_id: int):
    db = _db()
    ok = crud.borrar_factura(db, factura_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    # Redirige al listado después de borrar
    return RedirectResponse(url="/facturas", status_code=303)
router = APIRouter()
templates = Jinja2Templates(directory="templates")

def _db() -> Session:
    return database.get_db()

# Home con menú
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Listado de facturas
@router.get("/facturas", response_class=HTMLResponse)
def listado(request: Request):
    db = _db()
    facturas = crud.listar_facturas(db)
    return templates.TemplateResponse("listado.html", {"request": request, "facturas": facturas})

# Formulario de subida
@router.get("/subir", response_class=HTMLResponse)
def subir_form(request: Request):
    return templates.TemplateResponse("subir.html", {"request": request})

# Procesar subida (UI)
@router.post("/facturas", response_class=HTMLResponse)
async def subir_factura(
    request: Request,
    file: UploadFile = File(...),
    destinatario_email: str | None = Body(None)
):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Formato no soportado. Use imágenes (PNG, JPG, JPEG).")

    try:
        txt = await ocr.extraer_texto(file)
        datos = ocr.procesar_campos(txt)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error de OCR: {e}")

    if not datos:
        raise HTTPException(status_code=422, detail="No se pudieron extraer los campos obligatorios.")

    db = _db()
    factura = crud.crear_factura(db, datos)

    if destinatario_email:
        try:
            html = plantilla_factura(factura)
            enviar_notificacion(destinatario_email, f"Nueva factura {factura.numero}", html)
        except Exception as e:
            print(f"[WARN] Error enviando email: {e}")

    return templates.TemplateResponse("factura.html", {"request": request, "factura": factura})

# Consultar factura en HTML
@router.get("/facturas/{factura_id}", response_class=HTMLResponse)
def consultar_factura(request: Request, factura_id: int):
    db = _db()
    factura = crud.obtener_factura(db, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return templates.TemplateResponse("factura.html", {"request": request, "factura": factura})

# Aprobar/Rechazar (GET desde correo para aprobación directa)
@router.get("/facturas/{factura_id}/decision", response_class=HTMLResponse)
def tomar_decision_via_link(
    request: Request,
    factura_id: int,
    estado: str = Query(..., pattern="^(Aprobado|Rechazado)$"),
    comentario: str | None = Query(None)
):
    db = _db()
    factura = crud.obtener_factura(db, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    factura, _ = transicionar_estado(factura, estado, comentario)
    factura = crud.actualizar_estado(db, factura, estado, comentario)
    return templates.TemplateResponse("factura.html", {"request": request, "factura": factura})

# Formulario de rechazo (desde correo) para capturar comentario
@router.get("/facturas/{factura_id}/rechazo", response_class=HTMLResponse)
def rechazar_form(request: Request, factura_id: int):
    db = _db()
    factura = crud.obtener_factura(db, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return templates.TemplateResponse("decision_rechazo.html", {"request": request, "factura": factura})

@router.post("/facturas/{factura_id}/rechazo", response_class=HTMLResponse)
def rechazar_submit(request: Request, factura_id: int, comentario: str = Body(...)):
    db = _db()
    factura = crud.obtener_factura(db, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    estado = "Rechazado"
    factura, _ = transicionar_estado(factura, estado, comentario)
    factura = crud.actualizar_estado(db, factura, estado, comentario)
    return RedirectResponse(url=f"/facturas/{factura_id}", status_code=303)
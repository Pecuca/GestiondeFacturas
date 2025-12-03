# 📑 Sistema de Gestión de Facturas con OCR y Notificaciones

Proyecto académico desarrollado con **FastAPI**, **Jinja2** y **Tesseract OCR**.  
Permite cargar facturas en formato imagen, extraer automáticamente los campos obligatorios, gestionarlas desde una interfaz web y enviar notificaciones interactivas por correo electrónico.

---

## 🚀 Características

- Carga de facturas en formato `.png` / `.jpg`.
- Extracción automática de:
  - Proveedor
  - Número de factura
  - Fecha de emisión
  - Monto total
  - Impuestos
  - Fecha de vencimiento
- Interfaz web con listado y detalle de facturas.
- Botones interactivos en correos:
  - **Aprobar** → cambia estado a *Aprobado*.
  - **Rechazar** → abre formulario para comentarios.
  - **Borrar** → elimina factura del sistema.
- Modo demo: vista previa de correos sin necesidad de SMTP real.

---

## 🛠️ Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/facturas-ocr.git
   cd facturas-ocr
   ```

2. Crea un entorno virtual e instala dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. Instala **Tesseract OCR**:
   - Windows: [UB Mannheim builds](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt install tesseract-ocr`
   - Mac: `brew install tesseract`

4. Configura la ruta en `ocr.py` si no está en el PATH:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```

5. Configura el correo remitente y su contraseña en `notifications.py`

---

## ▶️ Uso

1. Inicia el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Abre en el navegador:
   ```
   http://127.0.0.1:8000/facturas
   ```

3. Funcionalidades:
   - **Subir factura** → OCR extrae datos.
   - **Listado** → ver todas las facturas.
   - **Detalle** → aprobar, rechazar o borrar.
   - **Correo demo** → vista previa con botones interactivos.

---

## 📸 Ejemplo de factura ficticia

```
Proveedor: Proveedor X
Factura 1234
Fecha: 01/12/2025
Monto: $1000
Impuestos: $160
Vencimiento: 15/12/2025
```

---

## 📚 Requisitos académicos cumplidos

- OCR con Tesseract.  
- Interfaz web con FastAPI + Jinja2.  
- Notificaciones interactivas con botones en correo.  
- CRUD completo (crear, listar, aprobar/rechazar, borrar).  

---

## 👨‍🏫 Autor

Proyecto desarrollado por **Alex** como entrega académica.  

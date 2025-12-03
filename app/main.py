from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from . import routes, database

app = FastAPI(title="Sistema Inteligente de Gestión de Facturas")

# Inicializar DB
database.init_db()

# Incluir rutas
app.include_router(routes.router)

# Servir archivos estáticos (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")
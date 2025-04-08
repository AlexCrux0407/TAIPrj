from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
from app.routes import router
from app.database import engine, SessionLocal, get_db
from app import models
from sqlalchemy import create_engine
import os

# Nuevas importaciones para el módulo de gestión comercial
from app.gestion_comercial.routes import router as gestion_router

# Crear todas las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

def init_data():
    db = SessionLocal()
    try:
        models.init_db(db)
    finally:
        db.close()

app = FastAPI(title="HeroVerse Comics")

init_data()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Incluir las rutas existentes
app.include_router(router)

# Incluir las nuevas rutas para el módulo de gestión comercial
app.include_router(gestion_router)

# Ruta principal
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
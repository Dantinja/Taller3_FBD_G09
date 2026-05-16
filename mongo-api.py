from datetime import datetime
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

app = FastAPI()

# Configuración de CORS para permitir peticiones desde cualquier cliente

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==========================================
# Configuración de Base de Datos
# ==========================================

client = MongoClient(os.environ["MONGO_URI"])
db = client["ISIS2304J05202610"]

# ==========================================
# Endpoints
# ==========================================

@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    """Retorna la lista de comentarios asociados a un bar."""
    comentarios = list(db["comentarios_bares"].find({"bar_id": bar_id}))
    for c in comentarios:
        c["_id"] = str(c["_id"])
    return comentarios


@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    """Crea un nuevo comentario para un bar específico."""
    datos['bar_id'] = bar_id
    datos['date'] = datetime.now(datetime.isoformat)
    resultado = db["comentarios_bares"].insert_one(datos)
    return {"inserted_id": str(resultado.inserted_id)}


@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    """Retorna todos los eventos de un bar."""
    eventos = list(db["eventos"].find({"bar_id": bar_id}))
    for e in eventos:
        e["_id"] = str(e["_id"])
    return eventos


@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    """Crea un nuevo evento para un bar específico."""
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now(datetime.isoformat)
    resultado = db["eventos"].insert_one(datos)
    return {"inserted_id": str(resultado.inserted_id)}
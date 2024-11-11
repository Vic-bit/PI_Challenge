from fastapi import FastAPI
from app.routers import ask

# Inicializar la aplicación
app = FastAPI()

# Incluir el router de preguntas
app.include_router(ask.router)

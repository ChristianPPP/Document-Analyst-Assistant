from fastapi import FastAPI
from app.routers.endpoints import router

app = FastAPI()
app.include_router(router)  # Endpoints disponibles en /gettextprompt y /getresponseia

@app.get("/")
def root():
    return {"message": "API funcionando. Usa /gettextprompt o /getresponseia"}

# Podrías añadir middleware, CORS, etc. aquí si lo necesitas
# Ejemplo:
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
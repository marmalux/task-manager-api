from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Tarea(BaseModel):
    #tarea_id:   Optional[int]
    titulo:     str
    completo:   bool

tareas = [{"tarea_id": 1,
            "titulo":   "crear rutas de API",
            "completo": False},
            {"tarea_id": 2,
            "titulo":   "mofificar rutas API",
            "completo": True},
            {"tarea_id": 3,
            "titulo":   "no morir en el intento",
            "completo": True}
            ]
contador = 4

@app.get("/tasks")
def todas_tareas():
    return tareas

@app.get("/tasks/{tarea_id}")
def obtener_tarea(tarea_id: int):
    for tarea in tareas:
        if tarea["tarea_id"] == tarea_id:
            return tarea
    return {"message":"tarea no encontrada"}


@app.post("/tasks")
def registrar_tarea(tarea: Tarea):
    global contador

    nueva_tarea = {
        "tarea_id": contador,
        "titulo":   tarea.titulo,
        "completo": tarea.completo

    }
    tareas.append(nueva_tarea)
    contador += 1
    return {"message":f"tarea {tarea.titulo} insertada"}
    

@app.delete("/tasks/{tarea_id}")
def eliminar_tarea(tarea_id: int):
    for i,tarea in enumerate(tareas):
        if tarea["tarea_id"] == tarea_id:
            del tareas[i]
            return "tarea eliminada"
    return {"message": f"tarea no encontrada"}

@app.put("/tasks/{tarea_id}")
def mod_tarea(tarea_id: int,tarea: Tarea):
    return {"message": f"tarea {tarea_id} modificada"}


from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional
import os
import oracledb


app = FastAPI()

# Credencials
load_dotenv()
us = os.getenv("DB_USER")
pw = os.getenv("DB_PASSWORD")
ds = os.getenv("DB_DSN")

class Tarea(BaseModel):
    #tarea_id:   Optional[int]
    titulo:     str
    completo:   int

@app.get("/tasks")
def todas_tareas():
    try:
        
        connection = oracledb.connect(user = us,password = pw, dsn=ds)
        cursor = connection.cursor()
        sql = 'SELECT * FROM TASKS'
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    
    except Exception as e:
        return {"message":str(e)}
    
    finally:
        cursor.close()
        connection.close()

@app.get("/tasks/{tarea_id}")
def obtener_tarea(tarea_id: int):
    connection = oracledb.connect(user = us,password = pw, dsn=ds)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM TASKS WHERE TAREA_ID = :tareaid
        """,
        {
            "tareaid": tarea_id
        }
    )
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row


@app.post("/tasks")
def registrar_tarea(tarea: Tarea):
    try:
        connection = oracledb.connect(user = us,password = pw, dsn=ds)
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO TASKS (TITULO,TERMINADO)
            VALUES(:titulo, :completo)
            """,
            {
                "titulo":   tarea.titulo,
                "completo": tarea.completo
            }
        )
        connection.commit()
        return {"message":"contenido agregado"}
    
    except Exception as e:
        return {"error":str(e)}
    finally:
        cursor.close()
        connection.close()

@app.delete("/tasks/{tarea_id}")
def eliminar_tarea(tarea_id: int):
    try:

        connection = oracledb.connect(user = us,password = pw, dsn=ds)
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM TASKS WHERE TAREA_ID = :tareaid
            """,
            {
                "tareaid": tarea_id
            }
        )
        connection.commit()

        afectados = cursor.rowcount
        if afectados == 0:
            return {"status": "fila no encontrada"}
        else:
            return {"status": "fila eliminada"}

    except Exception as e:
        return {"error":str(e)}
    finally:
        cursor.close()
        connection.close()

@app.put("/tasks/{tarea_id}")
def mod_tarea(tarea_id: int,tarea: Tarea):

    try:
        connection = oracledb.connect(user = us,password = pw, dsn=ds)
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE TASKS SET TITULO = :titulo, TERMINADO = :completo WHERE TAREA_ID = :tareaid
            """,
            {
                "titulo": tarea.titulo,
                "completo": tarea.completo,
                "tareaid": tarea_id
            }
        )

        connection.commit()
        afectados = cursor.rowcount
        
        if afectados == 0:
            return {"status": "fila no encontrada"}
        else:
            return {"status": "fila editada"}
        
    except Exception as e:
        return {"error":str(e)}
    finally:
        cursor.close()
        connection.close()



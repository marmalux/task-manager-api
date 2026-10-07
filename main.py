from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
import oracledb
import os

app = FastAPI()

#Use Thick mode for connection to Oracle Autonomous Database
oracledb.init_oracle_client(
    lib_dir="/opt/oracle/instantclient_23_26",
    config_dir="/app/Wallet"
)
# Credencials
# load_dotenv()     Charge enviroment variables in python 

us = os.getenv("DB_USER")
pw = os.getenv("DB_PASSWORD")
ds = os.getenv("DB_DSN")
config_dir = "/app/Wallet"
wallet_pw = os.getenv("WALLET_PASSWORD")

class Tarea(BaseModel):
    titulo:     str
    completo:   int

#endpoints

@app.get("/tasks")
def todas_tareas():
    try:
        connection = oracledb.connect(user = us,password = pw, dsn=ds,config_dir=config_dir,wallet_password = wallet_pw,wallet_location=config_dir)
        cursor = connection.cursor()
        sql = 'SELECT * FROM TAREAS'        
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    
    except Exception as e:
        return {"message":str(e)}
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@app.get("/tasks/{tarea_id}")
def obtener_tarea(tarea_id: int):
    connection = oracledb.connect(user = us,password = pw, dsn=ds,config_dir=config_dir,wallet_password = wallet_pw,wallet_location=config_dir)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM TAREAS WHERE TAREA_ID = :tareaid      
        """,
        {
            "tareaid": tarea_id                 #SQL Parameters
        }
    )
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row


@app.post("/tasks")
def registrar_tarea(tarea: Tarea):
    try:
        connection = oracledb.connect(user = us,password = pw, dsn=ds,config_dir=config_dir,wallet_password = wallet_pw,wallet_location=config_dir)
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO TAREAS (TITULO,TERMINADO)
            VALUES(:titulo, :completo)
            """,
            {
                "titulo":   tarea.titulo,                   #SQL Parameters
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
        connection = oracledb.connect(user = us,password = pw, dsn=ds,config_dir=config_dir,wallet_password = wallet_pw,wallet_location=config_dir)
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM TAREAS WHERE TAREA_ID = :tareaid
            """,
            {
                "tareaid": tarea_id             #SQL Parameters
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
        connection = oracledb.connect(user = us,password = pw, dsn=ds,config_dir=config_dir
                                      ,wallet_password = wallet_pw,wallet_location=config_dir)
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE TAREAS SET TITULO = :titulo, TERMINADO = :completo WHERE TAREA_ID = :tareaid
            """,
            {
                "titulo": tarea.titulo,                 #SQL Parameters
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



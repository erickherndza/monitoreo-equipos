from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import psycopg2
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

security = HTTPBearer()
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Token inválido")

def guardar_en_db(data):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO monitoreo (equipo_id, timestamp, lat, lon, rpm, temperatura, combustible, errores)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data["equipo_id"],
        datetime.fromisoformat(data["timestamp"]),
        data["gps"]["lat"],
        data["gps"]["lon"],
        data["rpm"],
        data["temperatura"],
        data["combustible"],
        json.dumps(data["errores"])
    ))
    conn.commit()
    cur.close()
    conn.close()

@app.post("/datos", dependencies=[Depends(verificar_token)])
async def recibir_datos(request: Request):
    data = await request.json()
    guardar_en_db(data)
    return {"status": "ok"}

@app.get("/ultimos")
async def ultimos():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    cur.execute("SELECT equipo_id, timestamp, lat, lon, rpm, temperatura, combustible, errores FROM monitoreo ORDER BY timestamp DESC LIMIT 20")
    filas = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "equipo_id": f[0],
            "timestamp": f[1],
            "lat": f[2],
            "lon": f[3],
            "rpm": f[4],
            "temperatura": f[5],
            "combustible": f[6],
            "errores": f[7]
        } for f in filas
    ]

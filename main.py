from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, ValidationError
from typing import List
import psycopg2
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Seguridad
security = HTTPBearer()
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != SECRET_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token inválido")

# Schema de datos con validación
class GPSData(BaseModel):
    lat: float
    lon: float

class EntradaMonitoreo(BaseModel):
    equipo_id: str = Field(..., min_length=1)
    timestamp: str
    gps: GPSData
    rpm: int = Field(..., ge=0)
    temperatura: float
    combustible: float
    errores: List[str] = []

# Conexión a base de datos como contexto
def obtener_conexion():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def guardar_en_db(data: EntradaMonitoreo):
    with obtener_conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO monitoreo (equipo_id, timestamp, lat, lon, rpm, temperatura, combustible, errores)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                data.equipo_id,
                datetime.fromisoformat(data.timestamp),
                data.gps.lat,
                data.gps.lon,
                data.rpm,
                data.temperatura,
                data.combustible,
                json.dumps(data.errores)
            ))

# Endpoint POST protegido
@app.post("/datos", dependencies=[Depends(verificar_token)])
async def recibir_datos(request: Request):
    try:
        payload = await request.json()
        entrada = EntradaMonitoreo(**payload)
        guardar_en_db(entrada)
        return {"status": "ok"}
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=f"Error de validación: {ve.errors()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")

# Endpoint GET de últimos registros
@app.get("/ultimos", dependencies=[Depends(verificar_token)])
async def ultimos():
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT equipo_id, timestamp, lat, lon, rpm, temperatura, combustible, errores
                    FROM monitoreo ORDER BY timestamp DESC LIMIT 20
                """)
                filas = cur.fetchall()

        return [
            {
                "equipo_id": f[0],
                "timestamp": f[1].isoformat(),
                "lat": f[2],
                "lon": f[3],
                "rpm": f[4],
                "temperatura": f[5],
                "combustible": f[6],
                "errores": f[7]
            } for f in filas
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo recuperar datos: {str(e)}")

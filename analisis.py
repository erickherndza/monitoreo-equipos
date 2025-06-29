import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
df = pd.read_sql("SELECT * FROM monitoreo ORDER BY timestamp DESC LIMIT 1000", conn)

alertas = df[df["temperatura"] > 90]
print("Equipos con sobrecalentamiento:")
print(alertas[["equipo_id", "temperatura", "timestamp"]])

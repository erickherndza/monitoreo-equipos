import requests
import time
import random
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

url = "http://localhost:8000/datos"
headers = {"Authorization": f"Bearer {os.getenv('SECRET_TOKEN')}"}

while True:
    data = {
        "equipo_id": "CAT330-FAKE",
        "timestamp": datetime.utcnow().isoformat(),
        "gps": {"lat": 18.4809, "lon": -69.9422},
        "rpm": random.randint(1000, 2000),
        "temperatura": random.uniform(70, 95),
        "combustible": random.randint(10, 100),
        "errores": []
    }
    response = requests.post(url, headers=headers, json=data)
    print("Enviado:", data)
    time.sleep(5)

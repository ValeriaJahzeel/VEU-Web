#!/usr/bin/env python3
# generar_reportes_fake.py
# ---------------------------------------------------------------
# Crea un CSV con registros sintéticos para la tabla `reporte`
# Ajusta:
#   • N          → número de filas a generar
#   • USERS      → lista de UUID válidos o [] si quieres dejar FK nula
#   • TIPOS      → ids existentes en tu tabla `tipo`
#   • bounding box de coordenadas
# ---------------------------------------------------------------
import pandas as pd
import numpy as np
from uuid import uuid4
from datetime import datetime, timedelta
import random

# -------------  CONFIGURACIÓN RÁPIDA  --------------------------
N      = 500                                    # registros a generar
TIPOS  = [1, 3, 6, 19, 27, 39, 44, 48, 52, 57]  # fk_reporte_tipo válidos

# ①  PON AQUÍ UUIDs REALES DE TU TABLA `reporte_users`
USERS  = [
    # "6eaf1c57-338a-48f0-a5b7-63e86966b4a4",
    # "777781de-b3e5-435d-b1ec-c338e2d534f2",
    "15ee040d-6e71-4459-82e6-00820161d282",
    "395f67a2-b8a9-45e5-91c4-cae02e66c936",
    "6d1cefac-504a-40ea-9983-cb638b3de3b3",
    "6eaf1c57-338a-48f0-a5b7-63e86966b4a4",
    "777781de-b3e5-435d-b1ec-c338e2d534f2",
    "7b30ab04-1271-42e2-8592-ad6ba56fe4c5",
    "8e3b954e-dc69-4721-b2f3-01613f067ce4",
    "aaa43b55-8601-41a6-b395-f04faeeef174",
    "c456ad34-ae59-4960-88f3-bb5b5f6f1783",
    "ce2bc421-50b4-46ee-97c3-dd7c3f7d62ad",
]
#  Si dejas USERS=[], se insertará NULL en fk_reporte_users
# ---------------------------------------------------------------

# Rango de fechas (últimos 6 meses)
hoy = datetime.now()
fecha_ini = hoy - timedelta(days=180)

def fecha_random():
    delta = hoy - fecha_ini
    return fecha_ini + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def coords():
    """Devuelve lat, lon dentro de la CDMX ~ ajusta a tu ciudad."""
    lat = np.random.uniform(19.3, 19.55)
    lon = np.random.uniform(-99.3, -99.05)
    return round(lat, 6), round(lon, 6)

rows = []
for _ in range(N):
    lat, lon = coords()
    f_crea   = fecha_random()
    # 30 % probabilidad de estar resuelto
    f_res    = f_crea + timedelta(hours=random.randint(1, 72)) if random.random() < 0.3 else None

    rows.append({
        # id_reporte se autogenera → NO lo incluimos
        "fk_reporte_users": random.choice(USERS) if USERS else None,
        "fk_reporte_tipo":  random.choice(TIPOS),
        "fecha_creacion":   f_crea.isoformat(),
        "fecha_resuelto":   f_res.isoformat() if f_res else None,
        "latitud":          lat,
        "longitud":         lon,
        "codigo_postal":    random.choice(["01000", "04200", "06470", "09030", None]),
    })

df = pd.DataFrame(rows)
df.to_csv("Fake_Data/reporte_fake.csv", index=False)
print("✅ CSV generado:", "Fake_Data/reporte_fake.csv", "con", len(df), "filas")

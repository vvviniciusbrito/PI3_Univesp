import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from statistics import mean, multimode

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sua URL do Neon
DATABASE_URL = "postgresql://neondb_owner:npg_B2k4wXWQZaNe@ep-summer-bread-acqeu0vl.sa-east-1.aws.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def classificar_pressao(media_sis, media_dia):
    """Lógica simplificada para classificação baseada em diretrizes de saúde."""
    if media_sis < 120 and media_dia < 80:
        return "Normal"
    elif 120 <= media_sis < 130 and media_dia < 80:
        return "Elevada"
    elif 130 <= media_sis < 140 or 80 <= media_dia < 90:
        return "Hipertensão Estágio 1"
    else:
        return "Hipertensão Estágio 2 / Crise"

@app.get("/consulta/{paciente_id}")
async def consultar_pressao(paciente_id: int, inicio: str, fim: str):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Buscamos as duas colunas agora
    query = """
        SELECT sistolica, diastolica FROM afericoes 
        WHERE paciente_id = %s AND data_hora BETWEEN %s AND %s
    """
    cur.execute(query, (paciente_id, inicio, fim))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return {"mensagem": "Nenhum dado encontrado"}

    # Separando os dados em duas listas
    sistolicas = [r[0] for r in rows]
    diastolicas = [r[1] for r in rows]
    
    media_sis = mean(sistolicas)
    media_dia = mean(diastolicas)

    return {
        "paciente_id": paciente_id,
        "frequencia_leituras": len(rows),
        "classificacao_baseada_na_media": classificar_pressao(media_sis, media_dia),
        "estatisticas_sistolica": {
            "media": round(media_sis, 2),
            "maximo": max(sistolicas),
            "minimo": min(sistolicas),
            "moda": multimode(sistolicas)
        },
        "estatisticas_diastolica": {
            "media": round(media_dia, 2),
            "maximo": max(diastolicas),
            "minimo": min(diastolicas),
            "moda": multimode(diastolicas)
        }
    }
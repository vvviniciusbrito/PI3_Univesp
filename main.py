import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from statistics import mean, mode, multimode

app = FastAPI()

# ESSENCIAL: Permite que o front do seu colega acesse sua API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Substitua pela sua URL do Neon (ou use variáveis de ambiente)
DATABASE_URL = "SUA_CONNECTION_STRING_AQUI"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.get("/consulta/{paciente_id}")
async def consultar_pressao(paciente_id: int, inicio: str, fim: str):
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = """
        SELECT sistolica FROM afericoes 
        WHERE paciente_id = %s AND data_hora BETWEEN %s AND %s
    """
    cur.execute(query, (paciente_id, inicio, fim))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    dados = [r[0] for r in rows]
    
    if not dados:
        return {"mensagem": "Nenhum dado encontrado"}

    return {
        "estatisticas": {
            "media": sum(dados) / len(dados),
            "frequencia": len(dados),
            "maximo": max(dados),
            "minimo": min(dados),
            "moda": multimode(dados) # Retorna uma lista com as modas
        }
    }
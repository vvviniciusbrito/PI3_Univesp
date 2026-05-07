import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from statistics import mean, stdev

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "postgresql://neondb_owner:npg_B2k4wXWQZaNe@ep-summer-bread-acqeu0vl.sa-east-1.aws.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def classificar_pressao(media_sis, media_dia):
    if media_sis < 120 and media_dia < 80:
        return "Normal"
    elif 120 <= media_sis < 130 and media_dia < 80:
        return "Elevada"
    elif 130 <= media_sis < 140 or 80 <= media_dia < 90:
        return "Hipertensão Estágio 1"
    else:
        return "Hipertensão Estágio 2 / Crise"

# Rota mais específica PRIMEIRO
@app.get("/consulta/{paciente_id}/todas")
async def consultar_pressao_todas(paciente_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT sistolica, diastolica, data_hora FROM afericoes 
        WHERE paciente_id = %s
        ORDER BY data_hora ASC
    """
    cur.execute(query, (paciente_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return {"mensagem": "Nenhum dado encontrado"}

    sistolicas = [r[0] for r in rows]
    diastolicas = [r[1] for r in rows]

    historico = []
    for r in rows:
        historico.append({
            "data": r[2].strftime("%Y-%m-%d %H:%M:%S"),
            "sistolica": r[0],
            "diastolica": r[1]
        })

    desvio_sis = stdev(sistolicas) if len(sistolicas) > 1 else 0.0
    desvio_dia = stdev(diastolicas) if len(diastolicas) > 1 else 0.0
    media_sis = mean(sistolicas)
    media_dia = mean(diastolicas)

    return {
        "paciente_id": paciente_id,
        "frequencia_leituras": len(rows),
        "classificacao_geral": classificar_pressao(media_sis, media_dia),
        "estatisticas": {
            "sistolica": {
                "media": round(media_sis, 2),
                "desvio_padrao": round(desvio_sis, 2),
                "maximo": max(sistolicas),
                "minimo": min(sistolicas)
            },
            "diastolica": {
                "media": round(media_dia, 2),
                "desvio_padrao": round(desvio_dia, 2),
                "maximo": max(diastolicas),
                "minimo": min(diastolicas)
            }
        },
        "lista_medicoes": historico
    }

# Rota genérica DEPOIS
@app.get("/consulta/{paciente_id}")
async def consultar_pressao(paciente_id: int, inicio: str, fim: str):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT sistolica, diastolica, data_hora FROM afericoes 
        WHERE paciente_id = %s AND data_hora BETWEEN %s AND %s
        ORDER BY data_hora ASC
    """
    cur.execute(query, (paciente_id, inicio, fim))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return {"mensagem": "Nenhum dado encontrado"}

    sistolicas = [r[0] for r in rows]
    diastolicas = [r[1] for r in rows]

    historico = []
    for r in rows:
        historico.append({
            "data": r[2].strftime("%Y-%m-%d %H:%M:%S"),
            "sistolica": r[0],
            "diastolica": r[1]
        })

    desvio_sis = stdev(sistolicas) if len(sistolicas) > 1 else 0.0
    desvio_dia = stdev(diastolicas) if len(diastolicas) > 1 else 0.0
    media_sis = mean(sistolicas)
    media_dia = mean(diastolicas)

    return {
        "paciente_id": paciente_id,
        "frequencia_leituras": len(rows),
        "classificacao_geral": classificar_pressao(media_sis, media_dia),
        "estatisticas": {
            "sistolica": {
                "media": round(media_sis, 2),
                "desvio_padrao": round(desvio_sis, 2),
                "maximo": max(sistolicas),
                "minimo": min(sistolicas)
            },
            "diastolica": {
                "media": round(media_dia, 2),
                "desvio_padrao": round(desvio_dia, 2),
                "maximo": max(diastolicas),
                "minimo": min(diastolicas)
            }
        },
        "lista_medicoes": historico
    }    query = """
        SELECT sistolica, diastolica, data_hora FROM afericoes 
        WHERE paciente_id = %s AND data_hora BETWEEN %s AND %s
        ORDER BY data_hora ASC
    """
    cur.execute(query, (paciente_id, inicio, fim))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return {"mensagem": "Nenhum dado encontrado"}

    # Listas auxiliares para cálculos
    sistolicas = [r[0] for r in rows]
    diastolicas = [r[1] for r in rows]
    
    # Criando a lista detalhada para o front-end (Gráficos)
    historico = []
    for r in rows:
        historico.append({
            "data": r[2].strftime("%Y-%m-%d %H:%M:%S"),
            "sistolica": r[0],
            "diastolica": r[1]
        })

    # Cálculo do Desvio Padrão (precisa de pelo menos 2 valores)
    desvio_sis = stdev(sistolicas) if len(sistolicas) > 1 else 0.0
    desvio_dia = stdev(diastolicas) if len(diastolicas) > 1 else 0.0

    media_sis = mean(sistolicas)
    media_dia = mean(diastolicas)

    return {
        "paciente_id": paciente_id,
        "frequencia_leituras": len(rows),
        "classificacao_geral": classificar_pressao(media_sis, media_dia),
        "estatisticas": {
            "sistolica": {
                "media": round(media_sis, 2),
                "desvio_padrao": round(desvio_sis, 2),
                "maximo": max(sistolicas),
                "minimo": min(sistolicas)
            },
            "diastolica": {
                "media": round(media_dia, 2),
                "desvio_padrao": round(desvio_dia, 2),
                "maximo": max(diastolicas),
                "minimo": min(diastolicas)
            }
        },
        "lista_medicoes": historico # Ideal para o colega montar o gráfico
    }

@app.get("/consulta/{paciente_id}/todas")
async def consultar_pressao_todas(paciente_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT sistolica, diastolica, data_hora FROM afericoes 
        WHERE paciente_id = %s
        ORDER BY data_hora ASC
    """
    cur.execute(query, (paciente_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return {"mensagem": "Nenhum dado encontrado"}

    sistolicas = [r[0] for r in rows]
    diastolicas = [r[1] for r in rows]

    historico = []
    for r in rows:
        historico.append({
            "data": r[2].strftime("%Y-%m-%d %H:%M:%S"),
            "sistolica": r[0],
            "diastolica": r[1]
        })

    desvio_sis = stdev(sistolicas) if len(sistolicas) > 1 else 0.0
    desvio_dia = stdev(diastolicas) if len(diastolicas) > 1 else 0.0
    media_sis = mean(sistolicas)
    media_dia = mean(diastolicas)

    return {
        "paciente_id": paciente_id,
        "frequencia_leituras": len(rows),
        "classificacao_geral": classificar_pressao(media_sis, media_dia),
        "estatisticas": {
            "sistolica": {
                "media": round(media_sis, 2),
                "desvio_padrao": round(desvio_sis, 2),
                "maximo": max(sistolicas),
                "minimo": min(sistolicas)
            },
            "diastolica": {
                "media": round(media_dia, 2),
                "desvio_padrao": round(desvio_dia, 2),
                "maximo": max(diastolicas),
                "minimo": min(diastolicas)
            }
        },
        "lista_medicoes": historico
    }

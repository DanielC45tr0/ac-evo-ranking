from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json
from datetime import datetime
import sqlite3
from pathlib import Path

app = FastAPI(title="AC Evo Ranking")

# ==================== BANCO DE DADOS ====================
def init_db():
    conn = sqlite3.connect("ranking.db")
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS races (
                    race_id TEXT PRIMARY KEY,
                    track TEXT,
                    date TEXT,
                    session_type TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY,
                    race_id TEXT,
                    driver_name TEXT,
                    driver_id TEXT,
                    position INTEGER,
                    points INTEGER DEFAULT 0,
                    best_lap TEXT,
                    total_time TEXT,
                    car TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ==================== RECEBER RESULTADO ====================
@app.post("/webhook/results")
async def receive_results(request: Request):
    try:
        data = await request.json()
        
        # Salva o JSON original (muito útil para debug)
        Path("last_result.json").write_text(
            json.dumps(data, indent=2, ensure_ascii=False), 
            encoding="utf-8"
        )
        
        print(f"✅ Resultado recebido às {datetime.now()}")
        print(f"   Sessão: {data.get('session_type', 'Desconhecido')} - Pista: {data.get('track', 'Desconhecida')}")
        
        # TODO: Vamos processar os resultados depois que você me mandar o JSON
        return {"status": "success", "message": "Resultado salvo"}
        
    except Exception as e:
        print(f"❌ Erro ao receber resultado: {e}")
        return {"status": "error"}

# ==================== PÁGINA DO RANKING ====================
@app.get("/", response_class=HTMLResponse)
async def ranking_page():
    conn = sqlite3.connect("ranking.db")
    c = conn.cursor()
    c.execute("""
        SELECT driver_name, SUM(points) as total_points 
        FROM results 
        GROUP BY driver_name, driver_id 
        ORDER BY total_points DESC
    """)
    ranking = c.fetchall()
    conn.close()

    html = """
    <html><head><meta charset="utf-8"><title>AC Evo Ranking</title>
    <style>body{font-family:Arial; margin:40px; background:#111; color:#ddd;}
    table{border-collapse:collapse; width:100%;} th, td{border:1px solid #555; padding:10px; text-align:center;}
    th{background:#222;}</style></head><body>
    <h1>🏆 Ranking Oficial - AC Evo</h1>
    <p>Atualizado automaticamente</p>
    <table>
        <tr><th>Posição</th><th>Piloto</th><th>Pontos Totais</th></tr>
    """
    for i, (nome, pontos) in enumerate(ranking, 1):
        html += f"<tr><td><b>{i}</b></td><td>{nome}</td><td><b>{pontos}</b></td></tr>"
    
    html += "</table></body></html>"
    return html

if __name__ == "__main__":
    print("🚀 Servidor AC Evo Ranking rodando!")
    print("Acesse: http://127.0.0.1:8000")


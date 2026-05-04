from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json
from datetime import datetime
import sqlite3
from pathlib import Path

app = FastAPI(title="VRB Racing")

# Banco simples
def init_db():
    conn = sqlite3.connect("ranking.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY,
                    driver_name TEXT,
                    points INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@app.post("/webhook/results")
async def receive_results(request: Request):
    data = await request.json()
    Path("last_result.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print("✅ Resultado recebido!")
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def ranking_page():
    html = """
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><title>VRB Racing</title>
    <style>
        body { background: #0a0a0a; color: #0f0; font-family: Arial; text-align: center; padding: 50px; }
        img { max-width: 420px; margin: 20px 0; }
        h1 { color: #00ff41; font-size: 3em; }
    </style>
    </head>
    <body>
        <img src="https://i.imgur.com/p4FCo8P.jpeg" alt="VRB">
        <h1>VRB - VIRTUAL RACING BOOST</h1>
        <h2>🏆 Ranking Oficial AC Evo</h2>
        <p><strong>Faça uma corrida no servidor para aparecer o ranking aqui.</strong></p>
        <p>Link atualizado em tempo real</p>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    print("VRB Ranking rodando")

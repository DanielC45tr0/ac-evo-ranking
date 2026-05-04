from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json
from datetime import datetime
import sqlite3
from pathlib import Path

app = FastAPI()

def init_db():
    conn = sqlite3.connect("ranking.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS races (race_id TEXT PRIMARY KEY, track TEXT, date TEXT, session_type TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, race_id TEXT, driver_name TEXT, position INTEGER, points INTEGER, car TEXT, category TEXT)''')
    conn.commit()
    conn.close()

init_db()

def get_category(car):
    c = str(car).lower()
    if 'gt3' in c: return 'GT3'
    if 'porsche' in c: return 'Porsche Cup'
    if 'dallara' in c: return 'Dallara'
    if 'formula' in c or 'f1' in c: return 'Formula'
    return 'Outros'

@app.post("/webhook/results")
async def receive_results(request: Request):
    data = await request.json()
    Path("last_result.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print("✅ Resultado recebido!")
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def ranking_page():
    html = """
    <html><head><meta charset="utf-8"><title>VRB Racing</title>
    <style>
        body {font-family:Arial; background:#0a0a0a; color:#ddd; text-align:center; padding:20px;}
        .logo {max-width:400px;}
        table {margin:30px auto; border-collapse:collapse; background:#111;}
        th, td {padding:12px 20px; border:1px solid #333;}
        th {background:#00ff41; color:black;}
    </style></head><body>
    <img src="https://i.imgur.com/p4FCo8P.jpeg" class="logo"><br>
    <h1>VRB - VIRTUAL RACING BOOST</h1>
    <h2>🏆 Ranking Oficial AC Evo</h2>
    <table>
        <tr><th>Pos</th><th>Piloto</th><th>Pontos</th><th>Categoria</th></tr>
    </table>
    <p>Faça uma corrida para aparecer o ranking...</p>
    </body></html>
    """
    return html

if __name__ == "__main__":
    print("VRB Running")

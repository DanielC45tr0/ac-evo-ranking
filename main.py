from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json
from datetime import datetime
import sqlite3
from pathlib import Path

app = FastAPI(title="VRB Racing")

def init_db():
    conn = sqlite3.connect("ranking.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS races (race_id TEXT PRIMARY KEY, track TEXT, date TEXT, session_type TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY, race_id TEXT, driver_name TEXT, driver_id TEXT,
                    position INTEGER, points INTEGER, car TEXT, category TEXT)''')
    conn.commit()
    conn.close()

init_db()

def calculate_points(pos):
    pts = [25,18,15,12,10,8,6,4,2,1]
    return pts[pos-1] if pos <= len(pts) else max(0, 10-pos)

def get_category(car):
    c = str(car).lower()
    if any(x in c for x in ['gt3','mercedes','bmw','audi','ferrari','lambo','mclaren']):
        return 'GT3'
    if 'porsche cup' in c or '911 cup' in c:
        return 'Porsche Cup'
    if 'dallara' in c:
        return 'Dallara'
    if any(x in c for x in ['formula','f1','f2','f3']):
        return 'Formula'
    if 'gt4' in c:
        return 'GT4'
    if 'tcr' in c:
        return 'TCR'
    return 'Outros'

@app.post("/webhook/results")
async def receive_results(request: Request):
    data = await request.json()
    Path("last_result.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    
    race_id = data.get("session_id") or str(datetime.now().timestamp())
    track = data.get("track", "Desconhecida")
    
    conn = sqlite3.connect("ranking.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO races VALUES (?,?,?,?)", 
             (race_id, track, datetime.now().isoformat(), data.get("session_type","Race")))
    
    results = data.get("results") or data.get("standings") or data.get("leaderboard") or []
    for r in results:
        name = r.get("driver_name") or r.get("name") or "Desconhecido"
        pos = int(r.get("position") or r.get("pos") or 0)
        car = r.get("car") or r.get("car_model") or r.get("vehicle") or "Desconhecido"
        cat = get_category(car)
        
        if pos > 0:
            points = calculate_points(pos)
            c.execute("INSERT INTO results (race_id,driver_name,position,points,car,category) VALUES (?,?,?,?,?,?)",
                     (race_id, name, pos, points, car, cat))
    
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def ranking_page():
    conn = sqlite3.connect("ranking.db")
    c = conn.cursor()
    c.execute("SELECT DISTINCT track FROM races ORDER BY date DESC")
    tracks = [row[0] for row in c.fetchall()]
    conn.close()

    html = f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="utf-8">
        <title>VRB Racing - Ranking Oficial</title>
        <style>
            body {{font-family:Arial,sans-serif; background:#0a0a0a; color:#ddd; margin:0;}}
            .header {{background:linear-gradient(#111,#000); padding:30px; text-align:center; border-bottom:6px solid #00ff41;}}
            .logo {{max-height:180px; filter:drop-shadow(0 0 20px #00ff41);}}
            h1 {{color:#00ff41; font-size:3em; margin:10px 0;}}
            .tabs {{display:flex; flex-wrap:wrap; gap:10px; justify-content:center; margin:30px 0;}}
            .tab {{padding:12px 25px; background:#1a1a1a; border:2px solid #333; border-radius:8px; cursor:pointer; font-weight:bold;}}
            .tab.active {{background:#00ff41; color:black; border-color:#00ff41;}}
            table {{width:100%; max-width:1100px; margin:20px auto; border-collapse:collapse; background:#111;}}
            th {{background:#00ff41; color:black; padding:16px;}}
            td {{padding:14px; text-align:center; border-bottom:1px solid #222;}}
            tr:hover {{background:#1f1f1f;}}
            .pos {{font-size:1.4em; font-weight:bold;}}
        </style>
    </head>
    <body>
        <div class="header">
            <img src="https://i.imgur.com/p4FCo8P.jpeg" class="logo" alt="VRB">
            <h1>VRB - VIRTUAL RACING BOOST</h1>
            <p>Ranking Oficial - Assetto Corsa Evo</p>
        </div>

        <div style="max-width:1100px; margin:auto; padding:20px;">
            <h2>🏆 Ranking por Categoria</h2>
            
            <div class="tabs">
                <div class="tab active" onclick="showCategory('all')">Geral</div>
                <div class="tab" onclick="showCategory('GT3')">GT3</div>
                <div class="tab" onclick="showCategory('Porsche Cup')">Porsche Cup</div>
                <div class="tab" onclick="showCategory('Dallara')">Dallara</div>
                <div class="tab" onclick="showCategory('Formula')">Formula</div>
                <div class="tab" onclick="showCategory('GT4')">GT4</div>
            </div>

            <table id="ranking">
                <tr><th>Pos</th><th>Piloto</th><th>Categoria</th><th>Carro</th><th>Pontos</th></tr>
            </table>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    print("VRB Ranking rodando!")

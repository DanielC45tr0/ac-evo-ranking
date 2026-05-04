from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="VRB")

@app.get("/", response_class=HTMLResponse)
async def ranking_page():
    return """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="utf-8">
        <title>VRB Racing - Ranking Oficial</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700&family=Roboto:wght@400;500&display=swap');
            
            body {
                background: linear-gradient(#0a0a0a, #000);
                color: #e0e0e0;
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                text-align: center;
            }
            .header {
                padding: 40px 20px;
                background: rgba(0, 0, 0, 0.8);
                border-bottom: 5px solid #00d4ff;
            }
            .logo {
                font-size: 5.5em;
                margin: 10px 0;
                filter: drop-shadow(0 0 30px #00d4ff);
            }
            h1 {
                font-family: 'Orbitron', sans-serif;
                color: #00d4ff;
                font-size: 3.2em;
                margin: 10px 0 5px;
                letter-spacing: 4px;
            }
            .subtitle {
                color: #00ff9d;
                font-size: 1.6em;
                margin-bottom: 30px;
            }
            .pista {
                color: #00ff9d;
                font-size: 1.4em;
                margin: 20px 0;
            }
            table {
                margin: 40px auto;
                border-collapse: collapse;
                width: 90%;
                max-width: 1100px;
                background: #111;
                box-shadow: 0 0 30px rgba(0, 212, 255, 0.2);
            }
            th {
                background: #00d4ff;
                color: black;
                padding: 18px;
                font-size: 1.1em;
            }
            td {
                padding: 16px;
                border-bottom: 1px solid #222;
            }
            tr:hover {
                background: #1a1a1a;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">🦅</div>
            <h1>VRB RACING</h1>
            <p class="subtitle">VIRTUAL RACING BOOST</p>
        </div>

        <p class="pista">🏁 Pista: Nenhuma corrida ainda</p>
        <h2>🏆 Ranking Oficial - Assetto Corsa Evo</h2>

        <table>
            <tr>
                <th>Posição</th>
                <th>Piloto</th>
                <th>Categoria</th>
                <th>Melhor Volta</th>
                <th>Média Limpa</th>
                 <th>Delta</th>
                 <th>Voltas</th>
            </tr>
        </table>

        <p style="margin-top:50px; color:#555;">Faça uma corrida no servidor para preencher o ranking</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    print("🚀 VRB Ranking rodando em http://127.0.0.1:8000")

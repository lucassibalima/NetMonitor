import time
ULTIMAS_METRICAS = {}
ULTIMAS_ATUALIZACOES = {}
from flask import Flask, render_template_string
import socket
import json
import threading
import os
app = Flask(__name__)
TOKEN = os.getenv("TOKEN", "netmonitor2026")

app = Flask(__name__)

ULTIMAS_METRICAS = {}
lock = threading.Lock()

HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>NetMonitor</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body {
            background: #101827;
            color: white;
            font-family: Arial;
            padding: 30px;
        }

        h1 {
            color: #38bdf8;
        }

        .container {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }

        .card {
            background: #1e293b;
            padding: 25px;
            border-radius: 12px;
            width: 220px;
        }

        .valor {
            font-size: 32px;
            color: #38bdf8;
        }

        .status {
            color: #4ade80;
        }
    </style>
</head>
<body>
    <h1>NetMonitor</h1>
    <p>Monitoramento centralizado de servidores</p>

    <h2>Servidores monitorados: {{ metricas|length }}</h2>

    {% if metricas %}
        <div class="container">
            {% for hostname, dados in metricas.items() %}
                <div class="card">
                    <h2>{{ hostname }}</h2>

                    <h3>CPU</h3>
                    <div class="valor">{{ dados.cpu }}%</div>

                    <h3>RAM</h3>
                    <div class="valor">{{ dados.ram }}%</div>

                    <h3>Disco</h3>
                    <div class="valor">{{ dados.disco }}%</div>

                    <p>Sistema: {{ dados.sistema }}</p>
                    <p>Última atualização: {{ dados.horario }}</p>
                    {% if dados.status == "Online" %}
    <p class="status">● Online</p>
{% else %}
    <p style="color: #f87171;">● Offline</p>
{% endif %}
                </div>
            {% endfor %}
        </div>
    {% else %}
        <h2>Aguardando dados dos agentes...</h2>
    {% endif %}
</body>
</html>
"""


def atender_agente(conexao, endereco):
    print(f"Agente conectado: {endereco}")
    buffer = b""

    try:
        with conexao:
            while True:
                dados = conexao.recv(4096)

                if not dados:
                    break

                buffer += dados

                while b"\n" in buffer:
                    mensagem, buffer = buffer.split(b"\n", 1)

                    if not mensagem.strip():
                        continue

                    try:
                        metricas = json.loads(mensagem.decode("utf-8"))

                        if metricas.get("token") != TOKEN:
                           print("Agente rejeitado: token inválido.")
                           continue

                        hostname = metricas.get("hostname")

                        if not hostname:
                            continue

                        with lock:
                            ULTIMAS_METRICAS[hostname] = metricas
                            ULTIMAS_ATUALIZACOES[hostname] = time.time()

                        print(f"Métricas recebidas de {hostname}")

                    except (json.JSONDecodeError, UnicodeDecodeError):
                        print("Mensagem inválida recebida.")

    except OSError as erro:
        print(f"Erro na conexão com {endereco}: {erro}")

    finally:
        print(f"Agente desconectado: {endereco}")


def receber_dados():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", 9000))
    servidor.listen()

    print("Servidor TCP aguardando agentes na porta 9000...")

    while True:
        conexao, endereco = servidor.accept()

        thread = threading.Thread(
            target=atender_agente,
            args=(conexao, endereco),
            daemon=True
        )

        thread.start()


@app.route("/")
def inicio():
    agora = time.time()

    with lock:
        metricas = ULTIMAS_METRICAS.copy()
        atualizacoes = ULTIMAS_ATUALIZACOES.copy()

    for hostname, dados in metricas.items():
        ultima_atualizacao = atualizacoes.get(hostname, 0)

        if agora - ultima_atualizacao <= 15:
            dados["status"] = "Online"
        else:
            dados["status"] = "Offline"

    return render_template_string(HTML, metricas=metricas)


if __name__ == "__main__":
    thread = threading.Thread(target=receber_dados, daemon=True)
    thread.start()

    app.run(host="0.0.0.0", port=5001, debug=False)

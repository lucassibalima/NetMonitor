
import psutil
import platform
import socket
import time
import json
import os
from datetime import datetime

SERVIDOR = os.getenv("SERVIDOR", "127.0.0.1")
PORTA = int(os.getenv("PORTA", "9000"))
TOKEN = os.getenv("TOKEN", "netmonitor2026")
NOME_AGENTE = os.getenv("NOME_AGENTE", socket.gethostname())


def coletar_metricas():
    rede = psutil.net_io_counters()

    metricas = {
        "token": TOKEN,
        "hostname": NOME_AGENTE,
        "sistema": platform.system(),
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disco": psutil.disk_usage("/").percent,
        "rede_enviada": rede.bytes_sent,
        "rede_recebida": rede.bytes_recv,
        "horario": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return metricas


def conectar_servidor():
    while True:
        try:
            print(f"Conectando ao servidor {SERVIDOR}:{PORTA}...")

            with socket.create_connection(
                (SERVIDOR, PORTA), timeout=5
            ) as conexao:

                print(f"Agente {NOME_AGENTE} conectado!")

                while True:
                    dados = coletar_metricas()
                    mensagem = json.dumps(dados) + "\n"

                    conexao.sendall(mensagem.encode("utf-8"))

                    print(f"Métricas de {NOME_AGENTE} enviadas!")

                    time.sleep(5)

        except (OSError, ConnectionError) as erro:
            print(f"Falha na conexão: {erro}")
            print("Tentando novamente em 5 segundos...")
            time.sleep(5)


if __name__ == "__main__":
    conectar_servidor()

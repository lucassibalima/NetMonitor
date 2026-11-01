
import socketserver
import json


HOST = "0.0.0.0"
PORT = 9000


class GerenciadorAgente(socketserver.BaseRequestHandler):

    def handle(self):
        print(f"\nAgente conectado: {self.client_address}")

        buffer = b""

        try:
            while True:
                dados = self.request.recv(4096)

                if not dados:
                    break

                buffer += dados

                while b"\n" in buffer:
                    mensagem, buffer = buffer.split(b"\n", 1)

                    if not mensagem.strip():
                        continue

                    try:
                        metricas = json.loads(mensagem.decode("utf-8"))

                        print("\n===== DADOS RECEBIDOS =====")

                        for nome, valor in metricas.items():
                            print(f"{nome}: {valor}")

                        print("===========================")

                    except json.JSONDecodeError:
                        print("Erro: mensagem JSON inválida.")

        except OSError as erro:
            print(f"Erro na conexão: {erro}")

        finally:
            print(f"Agente desconectado: {self.client_address}")


class ServidorTCP(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":

    with ServidorTCP((HOST, PORT), GerenciadorAgente) as servidor:

        print("==============================")
        print(" NETMONITOR - SERVIDOR TCP")
        print("==============================")
        print(f"Servidor iniciado na porta {PORT}")
        print("Aguardando conexões dos agentes...")

        try:
            servidor.serve_forever()

        except KeyboardInterrupt:
            print("\nEncerrando servidor...")

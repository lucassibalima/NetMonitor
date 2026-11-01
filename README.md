# NetMonitor

## Sistema Centralizado de Monitoramento de Servidores

### 1. Sobre o projeto

O NetMonitor é um sistema de monitoramento centralizado desenvolvido em Python. Seu objetivo é acompanhar o desempenho de diferentes computadores por meio da coleta e transmissão de métricas para um servidor central.

Os dados recebidos são apresentados em um painel web, permitindo acompanhar a disponibilidade e o desempenho dos agentes monitorados.

Projeto desenvolvido para a disciplina PSI129A – Conectividade em Sistemas Ciberfísicos, da PUCPR.

### 2. Funcionalidades

- Monitoramento de CPU.
- Monitoramento de memória RAM.
- Monitoramento de disco.
- Coleta de informações de rede.
- Identificação do sistema operacional.
- Comunicação TCP entre agentes e servidor.
- Recebimento simultâneo de dados de múltiplos agentes.
- Dashboard web com atualização automática.
- Identificação dos agentes Online e Offline.
- Reconexão automática após falhas de comunicação.
- Autenticação básica por token.

### 3. Tecnologias utilizadas

- Python
- Flask
- Socket TCP
- JSON
- Psutil
- Docker
- Docker Compose
- HTML e CSS
- Linux

### 4. Arquitetura

O sistema utiliza uma arquitetura cliente-servidor.

Os agentes coletam informações dos computadores e enviam os dados ao servidor central por meio de conexões TCP.

O servidor valida o token recebido, processa as métricas e atualiza o dashboard.

Atualmente, o ambiente possui três agentes:

- MacBookPro: agente executado diretamente no macOS.
- Servidor-Linux-1: agente executado em container Docker.
- Servidor-Linux-2: agente executado em container Docker.

Os dois containers Linux são executados sobre o mesmo computador host.

### 5. Estrutura do projeto

    NetMonitor/
    ├── agent/
    │   └── agent.py
    ├── server/
    │   └── server.py
    ├── dashboard/
    │   └── app.py
    ├── docs/
    ├── evidence/
    ├── requirements.txt
    ├── docker-compose.yml
    ├── Dockerfile
    ├── README.md
    └── .gitignore

### 6. Como executar

#### Requisitos

- Python 3.12 ou superior.
- Docker.
- Docker Compose.

#### Instalar dependências

Na pasta principal do projeto, execute:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

#### Iniciar o dashboard

    .venv/bin/python dashboard/app.py

Acesse pelo navegador:

<http://127.0.0.1:5001>

O servidor TCP recebe as conexões dos agentes pela porta 9000.

#### Iniciar os agentes Docker

Em outro terminal, execute:

    docker compose build
    docker compose up -d

#### Iniciar o agente local

Opcionalmente, execute:

    .venv/bin/python agent/agent.py

### 7. Segurança

O sistema possui autenticação básica por token compartilhado entre os agentes e o servidor.

Cada agente envia seu token junto com as métricas. O servidor verifica o valor recebido e rejeita mensagens com tokens inválidos.

Também existe tratamento de falhas de conexão e tentativa automática de reconexão.

A implementação atual utiliza TCP sem criptografia TLS. Portanto, o token e as métricas são transmitidos sem proteção criptográfica.

### 8. Testes realizados

Foram realizados testes de:

1. Comunicação TCP entre agentes e servidor.
2. Envio e recebimento de métricas.
3. Monitoramento simultâneo de três agentes.
4. Atualização automática do dashboard.
5. Interrupção do servidor e reconexão automática.
6. Interrupção de um agente e identificação do status Offline.
7. Reinicialização de um agente e recuperação do status Online.
8. Autenticação com token válido.
9. Rejeição de token inválido.

### 9. Melhorias futuras

- Implementação de criptografia TLS.
- Armazenamento histórico das métricas em banco de dados.
- Gráficos de desempenho.
- Sistema de alertas para situações críticas.
- Melhorias na interface do dashboard.
- Implementação de autenticação mais avançada.

### 10. Conclusão

O NetMonitor demonstra a aplicação prática dos conceitos de conectividade, comunicação cliente-servidor, programação em Python, monitoramento de sistemas e infraestrutura com Docker.

O projeto permite acompanhar diferentes agentes por meio de uma plataforma centralizada, apresentando métricas em tempo real e identificando falhas de comunicação.

Com isso, foi possível desenvolver e testar uma solução funcional de monitoramento, aplicando os conhecimentos estudados na disciplina.

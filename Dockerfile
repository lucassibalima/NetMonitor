FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir psutil==7.2.2

COPY agent/agent.py /app/agent.py

CMD ["python", "-u", "agent.py"]
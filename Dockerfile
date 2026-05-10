FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY telegram_letta_bridge.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "telegram_letta_bridge.py"]

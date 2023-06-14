FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
COPY .env .
COPY bardBot.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bardBot.py"]

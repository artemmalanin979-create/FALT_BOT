FROM python:3.11-slim

WORKDIR /app

# Системные зависимости для matplotlib и pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p database logs data

CMD ["python", "start_all.py"]

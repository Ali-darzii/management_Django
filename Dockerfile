FROM python:3.11.6-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/PY/BIN:$PATH"

RUN pip install --upgrade pip

COPY ./req.txt /app/req.txt
COPY . /app


# installing libpq-dev and gcc  for postgres
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install -r req.txt

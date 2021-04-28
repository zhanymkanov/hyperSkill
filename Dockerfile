FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y gcc git libpq-dev libmagic1 netcat && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8

COPY requirements/ /requirements

RUN pip install -U pip && \
    pip install --no-cache-dir -r /requirements/base.txt

COPY . /proj

RUN chmod +x /proj/wait-for &&  mv /proj/wait-for /bin/wait-for

RUN useradd -m -d /proj -s /bin/bash app && \
    chown -R app:app /proj/*
WORKDIR /proj
USER app



FROM python:3.11-slim

RUN pip install --no-cache-dir matplotlib pandas numpy

WORKDIR /workspace
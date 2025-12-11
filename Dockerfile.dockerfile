FROM python:3.10-slim

WORKDIR /app

COPY entrypoint.py /app/entrypoint.py

RUN pip install requests pandas

ENTRYPOINT ["python", "/app/entrypoint.py"]

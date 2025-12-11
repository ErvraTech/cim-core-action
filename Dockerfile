FROM python:3.10-slim

# On se place dans le workspace GitHub
WORKDIR /github/workspace

# On copie seulement le script d'entrée
COPY entrypoint.py /github/workspace/entrypoint.py

# Dépendances Python
RUN pip install --no-cache-dir requests pandas

# Lancer le script
ENTRYPOINT ["python", "/github/workspace/entrypoint.py"]

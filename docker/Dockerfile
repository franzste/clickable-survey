# Verwende das offizielle Python-Image als Basis
FROM python:3.9-slim

# Setze das Arbeitsverzeichnis in /app
WORKDIR /app

# Kopiere die Abhängigkeiten in das Arbeitsverzeichnis
COPY requirements.txt .

# Installiere die Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest des Codes in das Arbeitsverzeichnis
COPY . .

# Setze den Umgebungsvariablen für Flask
ENV FLASK_APP=app.py

# Exponiere den Port 5000
EXPOSE 5000

# Starte die Flask-Anwendung
CMD ["python3", "docker/app/app.py", "--host=0.0.0.0"]

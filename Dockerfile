# Utiliser une image Python officielle comme image de base
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances
RUN python3.12 -m venv venv
RUN . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Copier le contenu de votre application dans le répertoire de travail
COPY . .

# Exposer le port sur lequel l'application s'exécutera
EXPOSE 8000

# Commande pour exécuter l'application
CMD ["sh", "-c", ". venv/bin/activate && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]


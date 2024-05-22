# Utiliser une image Python officielle comme image de base
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Mettre à jour la liste des packages
RUN apt update 

# Installer python3-pip
RUN apt install -y python3-pip

# Copier les fichiers dans le répertoire de travail
COPY requirements.txt /app

# Mettre à jour pip et installer les dépendances
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Copier les fichiers dans le répertoire de travail
COPY /verification_system /app

# Makemigrations
RUN python3 manage.py makemigrations

# Exposer le port sur lequel l'application s'exécutera
EXPOSE 8000

# Commande pour exécuter l'application
CMD ["sh", "-c", "python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]


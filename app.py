import os
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, session, jsonify, url_for, request
# from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Visiteur, Fournisseur, Automobile
from config import config
from datetime import datetime

# Créer une instance de l'application Flask

app = Flask(__name__)
env_type = 'development'
secret_key = os.urandom(24).hex()
app.secret_key = secret_key
app.config.from_object(config[env_type])
db.init_app(app)
# migrate = Migrate(app, db)

# Création des tables
with app.app_context():
    db.create_all()

CORS(app)  # Pour autoriser les requêtes CORS

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Définir une route pour la page d'accueil
@app.route('/')
def home():
    return "Hello, Flask!"

# Exécuter l'application Flask lorsque ce fichier est exécuté
if __name__ == '__main__':
    app.run()

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

## GESTION DE L'AUTHENTICATION
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("get_user_info", _external=True)  # Remplacez par votre URL de redirection
    )

@app.route("/users")
def get_user_info():
    # Vérifier si l'authentification a réussi
    token = oauth.auth0.authorize_access_token()
    if token:
        # Authentification réussie
        userinfo = oauth.auth0.parse_id_token(token, nonce=request.args.get('nonce'))
        # Vous pouvez accéder aux informations de l'utilisateur à partir de userinfo, par exemple :
        return jsonify({'message': 'Authentification réussie', 'userinfo': userinfo})
    else:
        # Authentification échouée
        return jsonify({'message': 'Échec de l\'authentification'})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": "http://localhost:5000",  # Remplacez par votre URL de redirection après la déconnexion
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route('/')
def index():
    return "Je suis une Application Flask deployer sur Heroku par Kteken"

# Routes pour les visiteurs
@app.route('/visiteurs', methods=['GET'])
def get_visiteurs():
    visiteurs = Visiteur.query.all()
    result = [
        {
            'id': visiteur.id,
            'nom': visiteur.nom,
            'email': visiteur.email,
            'numero_telephone': visiteur.numero_telephone,
            'photo_profil': visiteur.photo_profil,
            'date_enregistrement': visiteur.date_enregistrement.isoformat()
        }
        for visiteur in visiteurs
    ]
    return jsonify(result)

@app.route('/visiteurs/<int:visiteur_id>', methods=['GET'])
def get_visiteur(visiteur_id):
    visiteur = Visiteur.query.get(visiteur_id)
    if visiteur:
        result = {
            'id': visiteur.id,
            'nom': visiteur.nom,
            'email': visiteur.email,
            'numero_telephone': visiteur.numero_telephone,
            'photo_profil': visiteur.photo_profil,
            'date_enregistrement': visiteur.date_enregistrement.isoformat()
        }
        return jsonify(result)
    else:
        return jsonify({'message': 'Visiteur non trouvé'})

@app.route('/visiteurs', methods=['POST'])
def create_visiteur():
    data = request.json
    visiteur = Visiteur(
        nom=data['nom'],
        email=data['email'],
        numero_telephone=data['numero_telephone'],
        photo_profil=data['photo_profil'],
        date_enregistrement=datetime.utcnow()
    )
    db.session.add(visiteur)
    db.session.commit()
    return jsonify({'message': 'Visiteur créé avec succès'})

@app.route('/visiteurs', methods=['DELETE'])
def delete_all_visiteurs():
    # Supprimer tous les enregistrements de visiteurs de la base de données
    db.session.query(Visiteur).delete()
    db.session.commit()
    
    return jsonify({'message': 'Tous les visiteurs ont été supprimés avec succès'})

# Routes pour les fournisseurs
@app.route('/fournisseurs', methods=['GET'])
def get_fournisseurs():
    fournisseurs = Fournisseur.query.all()
    result = [
        {
            'id': fournisseur.id,
            'nom_fournisseur': fournisseur.nom_fournisseur,
            'email': fournisseur.email,
            'numero_telephone': fournisseur.numero_telephone,
            'logo_fournisseur': fournisseur.logo_fournisseur,
            'date_enregistrement': fournisseur.date_enregistrement.isoformat(),
            'localisation': fournisseur.localisation,
            'adresse': fournisseur.adresse
        }
        for fournisseur in fournisseurs
    ]
    return jsonify(result)

@app.route('/fournisseurs/<int:fournisseur_id>', methods=['GET'])
def get_fournisseur(fournisseur_id):
    fournisseur = Fournisseur.query.get(fournisseur_id)
    if fournisseur:
        result = {
            'id': fournisseur.id,
            'nom_fournisseur': fournisseur.nom_fournisseur,
            'email': fournisseur.email,
            'numero_telephone': fournisseur.numero_telephone,
            'logo_fournisseur': fournisseur.logo_fournisseur,
            'date_enregistrement': fournisseur.date_enregistrement.isoformat(),
            'localisation': fournisseur.localisation,
            'adresse': fournisseur.adresse
        }
        return jsonify(result)
    else:
        return jsonify({'message': 'Fournisseur non trouvé'})

@app.route('/fournisseurs', methods=['POST'])
def create_fournisseur():
    data = request.json
    fournisseur = Fournisseur(
        nom_fournisseur=data['nom_fournisseur'],
        email=data['email'],
        numero_telephone=data['numero_telephone'],
        logo_fournisseur=data['logo_fournisseur'],
        date_enregistrement=datetime.utcnow(),
        localisation=data['localisation'],
        adresse=data['adresse']
    )
    db.session.add(fournisseur)
    db.session.commit()
    return jsonify({'message': 'Fournisseur créé avec succès'})

@app.route('/fournisseurs', methods=['DELETE'])
def delete_all_fournisseurs():
    # Supprimer tous les enregistrements de fournisseurs de la base de données
    db.session.query(Fournisseur).delete()
    db.session.commit()
    
    return jsonify({'message': 'Tous les fournisseurs ont été supprimés avec succès'})

# Routes pour les automobiles
@app.route('/automobiles', methods=['GET'])
def get_automobiles():
    automobiles = Automobile.query.all()

    result = [
        {
            'id': automobile.id,
            'marque': automobile.marque,
            'prix': float(automobile.prix),
            'type_vehicule': automobile.type_vehicule,
            'couleur': automobile.couleur,
            'duree': get_duration(automobile.date_enregistrement),
            'fournisseur_id': automobile.fournisseur_id,
            'image': automobile.image
        }
        for automobile in automobiles
    ]
    return jsonify(result)


def get_duration(date_enregistrement):
    delta = datetime.now() - date_enregistrement
    duration = f"{delta.days} jours, {delta.seconds // 3600} heures, {(delta.seconds // 60) % 60} minutes"
    return duration

@app.route('/automobiles/<int:automobile_id>', methods=['GET'])
def get_automobile(automobile_id):
    automobile = Automobile.query.get(automobile_id)
    if automobile:
        result = {
            'id': automobile.id,
            'marque': automobile.marque,
            'prix': float(automobile.prix),
            'type_vehicule': automobile.type_vehicule,
            'couleur': automobile.couleur,
            'duree': (datetime.now().date() - automobile.date_enregistrement.date()).days,
            'fournisseur_id': automobile.fournisseur_id,
            'image': automobile.image
        }
        return jsonify(result)
    else:
        return jsonify({'message': 'Automobile non trouvée'})

@app.route('/automobiles', methods=['POST'])
def create_automobile():
    data = request.json

    # Créer une nouvelle instance de l'automobile
    automobile = Automobile(
        marque=data['marque'],
        prix=data['prix'],
        type_vehicule=data['type_vehicule'],
        couleur=data['couleur'],
        date_enregistrement=datetime.utcnow(),
        fournisseur_id=data['fournisseur_id'],
        image=data['image']
    )

    # Enregistrer l'automobile et ses images dans la base de données
    db.session.add(automobile)
    db.session.commit()

    return jsonify({'message': 'Automobile créée avec succès'})

@app.route('/automobiles', methods=['DELETE'])
def delete_all_automobiles():
    # Supprimer tous les enregistrements d'automobiles de la base de données
    db.session.query(Automobile).delete()
    db.session.commit()
    
    return jsonify({'message': 'Tous les automobiles ont été supprimés avec succès'})

@app.route('/recherche', methods=['GET'])
def recherche():
    # Récupérer les critères de recherche de la requête
    type_vehicule = request.args.get('type_vehicule')
    marque = request.args.get('marque')
    couleur = request.args.get('couleur')
    fournisseur = request.args.get('fournisseur')

    # Construire la requête de recherche
    query = db.session.query(Automobile)

    if type_vehicule:
        query = query.filter(Automobile.type_vehicule == type_vehicule)
    if marque:
        query = query.filter(Automobile.marque == marque)
    if couleur:
        query = query.filter(Automobile.couleur == couleur)
    if fournisseur:
        query = query.join(Automobile.fournisseur).filter(Fournisseur.nom_fournisseur == fournisseur)

    # Exécuter la requête
    result = query.all()

    # Formatter les résultats en JSON
    automobiles = []
    for automobile in result:
        automobiles.append({
            'id': automobile.id,
            'marque': automobile.marque,
            'prix': str(automobile.prix),
            'type_vehicule': automobile.type_vehicule,
            'couleur': automobile.couleur,
            'fournisseur': automobile.fournisseur.nom_fournisseur,
            'image': automobile.image
        })

    return jsonify(automobiles)

if __name__ == "__main__":
    app.run()

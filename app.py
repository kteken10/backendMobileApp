import os
import jwt
from jwt import encode as jwt_encode, decode as jwt_decode
from os import environ as env
from models import db, Visiteur, Fournisseur, Automobile
from dotenv import find_dotenv, load_dotenv
from flask import Flask,  jsonify, request
from flask_migrate import Migrate
# from flask_migrate import Migrate
from flask_cors import CORS

from config import config
from datetime import datetime, timedelta

app = Flask(__name__)
env_type = 'production'
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

secret_key = "T0pS3cr3tK3y!#"
app.secret_key = secret_key
app.config.from_object(config[env_type])
db.init_app(app)

# Création des tables
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)
CORS(app)  # Pour autoriser les requêtes CORS


@app.route('/')
def index():
    return "Je suis une Application Flask "

# Routes pour les visiteurs
@app.route('/visiteurs', methods=['POST'])
def create_visiteur():
    data = request.get_json()
    visiteur = Visiteur(
        nom=data['nom'],
        email=data['email'],
        numero_telephone=data['numero_telephone'],
        password=data['password'],
        date_enregistrement=datetime.utcnow(),
    )
    db.session.add(visiteur)
    db.session.commit()
    return jsonify({'message': 'Visiteur created successfully'})

@app.route('/visiteurs', methods=['GET'])
def get_visiteurs():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token missing'}), 401

    try:
        decoded_token = jwt_decode(token, secret_key, algorithms=['HS256']) # type: ignore
        user_id = decoded_token['user_id']

        visiteurs = Visiteur.query.all()
        result = [
            {
                'id': visiteur.id,
                'nom': visiteur.nom,
                'email': visiteur.email,
                'numero_telephone': visiteur.numero_telephone,
                'photo_profil': visiteur.photo_profil,
                'password': visiteur.password,
                'date_enregistrement': visiteur.date_enregistrement.isoformat()
            }
            for visiteur in visiteurs
        ]
        return jsonify(result)

    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    


@app.route('/visiteurs/<int:visiteur_id>', methods=['GET'])
def get_visiteur(visiteur_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token missing'}), 401

    try:
        decoded_token = jwt_decode(token, secret_key, algorithms=['HS256'])
        user_id = decoded_token['user_id']

        visiteur = Visiteur.query.get(visiteur_id)
        if visiteur:
            result = {
                'id': visiteur.id,
                'nom': visiteur.nom,
                'email': visiteur.email,
                'numero_telephone': visiteur.numero_telephone,
                'photo_profil': visiteur.photo_profil,
                'password': visiteur.password,
                'date_enregistrement': visiteur.date_enregistrement.isoformat()
            }
            return jsonify(result)
        else:
            return jsonify({'message': 'Visiteur non trouvé'})

    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

@app.route('/visiteurs', methods=['DELETE'])
def delete_all_visiteurs():
    # Supprimer tous les enregistrements de visiteurs de la base de données
    db.session.query(Visiteur).delete()
    db.session.commit()
    
    return jsonify({'message': 'Tous les visiteurs ont été supprimés avec succès'})

# Routes pour l'authentification fournisseur et visiteur
@app.route('/auth', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    email = data['email']
    password = data['password']

    visiteur = Visiteur.query.filter_by(email=email).first()
    fournisseur = Fournisseur.query.filter_by(email=email).first()
    if visiteur and visiteur.password == password:
        token = generate_token(visiteur.id)
        return jsonify({'user_type': 'visiteur', 'token': token,'user_id': visiteur.id})

    elif fournisseur and fournisseur.password == password:
        token = generate_token(fournisseur.id)
        return jsonify({'user_type': 'fournisseur', 'token': token , 'user_id': fournisseur.id})

    return jsonify({'message': 'Invalid credentials'}), 401


def generate_token(user_id):
    user_id=user_id
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt_encode(payload, secret_key, algorithm='HS256') # type: ignore
    return token 


# Routes pour les fournisseurs

@app.route('/fournisseurs', methods=['POST'])
def create_fournisseur():
    data = request.get_json()
    fournisseur = Fournisseur(
        nom_fournisseur=data['nom_fournisseur'],
        email=data['email'],
        numero_telephone=data['numero_telephone'],
        date_enregistrement=datetime.utcnow(),
        logo_fournisseur=data['logo_fournisseur'],
        password=data['password'],
        localisation=data['localisation'],
        adresse=data['adresse']
    )
    db.session.add(fournisseur)
    db.session.commit()
    return jsonify({'message': 'Fournisseur created successfully'})
@app.route('/fournisseurs', methods=['GET'])
def get_fournisseurs():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token missing'}), 401

    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = decoded_token['user_id']

        fournisseurs = Fournisseur.query.all()
        result = [
            {
                'id': fournisseur.id,
                'nom': fournisseur.nom,
                'email': fournisseur.email,
                'numero_telephone': fournisseur.numero_telephone,
                'photo_profil': fournisseur.photo_profil,
                'password': fournisseur.password,
                'date_enregistrement': fournisseur.date_enregistrement.isoformat()
            }
            for fournisseur in fournisseurs
        ]
        return jsonify(result)

    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401



@app.route('/fournisseurs', methods=['DELETE'])
def delete_all_fournisseurs():
    # Supprimer tous les enregistrements de fournisseurs de la base de données
    db.session.query(Fournisseur).delete()
    db.session.commit()
    
    return jsonify({'message': 'Tous les fournisseurs ont été supprimés avec succès'})

# Routes pour les automobiles

@app.route('/automobiles', methods=['POST'])
def create_automobile():
    data = request.get_json()

    # Créer une nouvelle instance de l'automobile
    automobile = Automobile(
        marque=data['marque'],
        prix=data['prix'],
        puissance_maximale=data['puissance_maximale'],
        vitesse_maximale=data['vitesse_maximale'],
        moteur=data['moteur'],
        type_vehicule=data['type_vehicule'],
        couleur=data['couleur'],
        date_enregistrement=datetime.utcnow(),
        fournisseur_id=data['fournisseur_id'],
        description=data['description'],
        image= data['image']
    )

    # Enregistrer l'automobile dans la base de données
    db.session.add(automobile)
    db.session.commit()

    return jsonify({'message': 'Automobile créée avec succès'})
@app.route('/automobiles', methods=['GET'])
def get_automobiles():
    automobiles = Automobile.query.all()

    result = [
        {
            'id': automobile.id,
            'marque': automobile.marque,
            'prix': float(automobile.prix),
            'puissance_maximale': float(automobile.puissance_maximale),
            'vitesse_maximale': float(automobile.vitesse_maximale),
            'moteur': float(automobile.moteur),
            'type_vehicule': automobile.type_vehicule,
            'couleur': automobile.couleur,
            'duree': get_duration(automobile.date_enregistrement),
            'fournisseur_info': {
                'id': automobile.fournisseur.id,
                'nom_fournisseur': automobile.fournisseur.nom_fournisseur,
                'email': automobile.fournisseur.email,
                'numero_telephone': automobile.fournisseur.numero_telephone,
                'logo_fournisseur': automobile.fournisseur.logo_fournisseur,
                'date_enregistrement': automobile.fournisseur.date_enregistrement,
                'localisation': automobile.fournisseur.localisation,
                'adresse': automobile.fournisseur.adresse
            },
            'description': automobile.description,
            'image': automobile.image
        }
        for automobile in automobiles
    ]
    return jsonify(result)

@app.route('/automobiles/<int:automobile_id>', methods=['GET'])
def get_automobile(automobile_id):
    automobile = Automobile.query.get(automobile_id)
    if automobile:
        result = {
            'id': automobile.id,
            'marque': automobile.marque,
            'prix': float(automobile.prix),
            'puissance_maximale': float(automobile.puissance_maximale),
            'vitesse_maximale': float(automobile.vitesse_maximale),
            'moteur': float(automobile.moteur),
            'type_vehicule': automobile.type_vehicule,
            'couleur': automobile.couleur,
            'duree': (datetime.now().date() - automobile.date_enregistrement.date()).days,
            'fournisseur_info': {
                'id': automobile.fournisseur.id,
                'nom_fournisseur': automobile.fournisseur.nom_fournisseur,
                'email': automobile.fournisseur.email,
                'numero_telephone': automobile.fournisseur.numero_telephone,
                'logo_fournisseur': automobile.fournisseur.logo_fournisseur,
                'date_enregistrement': automobile.fournisseur.date_enregistrement,
                'localisation': automobile.fournisseur.localisation,
                'adresse': automobile.fournisseur.adresse
            },
            'description': automobile.description,
            'image': automobile.image
        }
        return jsonify(result)
    else:
        return jsonify({'message': 'Automobile non trouvée'})
    
#Compter le nombre de voiture d'un fournisseur     

@app.route("/fournisseurs/<int:user_id>/vehicle-count", methods=["GET"])
def get_vehicle_count(user_id):
    fournisseur = Fournisseur.query.get(user_id)
    if fournisseur is None:
        return jsonify({"error": "Fournisseur not found"}), 404

    vehicle_count = len(fournisseur.automobiles)
    return jsonify({"count": vehicle_count})

#Supprimer une voiture connaissant son ID 
@app.route("/vehicles/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id):
    try:
        # Recherche du véhicule à supprimer dans la base de données
        vehicle = Automobile.query.get(vehicle_id)

        if vehicle:
            # Suppression du véhicule
            db.session.delete(vehicle)
            db.session.commit()

            return jsonify({"message": "Véhicule supprimé avec succès"})
        else:
            return jsonify({"error": "Véhicule non trouvé"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Récupérer un véhicule connaissant l'id de son fournisseur 
@app.route('/fournisseurs/<int:fournisseur_id>/vehicles', methods=['GET'])
def get_fournisseur_vehicles(fournisseur_id):
    vehicles = Automobile.query.filter_by(fournisseur_id=fournisseur_id).all()
    result = []
    for vehicle in vehicles:
        vehicle_data = {
            'id': vehicle.id,
            'marque': vehicle.marque,
            'prix': float(vehicle.prix),
            'puissance_maximale': float(vehicle.puissance_maximale),
            'vitesse_maximale': float(vehicle.vitesse_maximale),
            'moteur': float(vehicle.moteur),
            'type_vehicule': vehicle.type_vehicule,
            'couleur': vehicle.couleur,
            'duree': (datetime.now().date() - vehicle.date_enregistrement.date()).days,
            'fournisseur_info': {
                'id': vehicle.fournisseur.id,
                'nom_fournisseur': vehicle.fournisseur.nom_fournisseur,
                'email': vehicle.fournisseur.email,
                'numero_telephone': vehicle.fournisseur.numero_telephone,
                'logo_fournisseur': vehicle.fournisseur.logo_fournisseur,
                'date_enregistrement': vehicle.fournisseur.date_enregistrement,
                'localisation': vehicle.fournisseur.localisation,
                'adresse': vehicle.fournisseur.adresse
            },
            'description': vehicle.description,
            'image': vehicle.image
        }
        result.append(vehicle_data)
    return jsonify(result)

@app.route('/automobiles', methods=['DELETE'])
def delete_all_automobiles():
    # Supprimer tous les enregistrements d'automobiles de la base de données
    db.session.query(Automobile).delete()
    db.session.commit()
    
    return jsonify({'message': 'Tous les automobiles ont été supprimés avec succès'})
# Route pour gérer la recherche de véhicule
@app.route('/recherche', methods=['GET'])
def recherche():
    # Récupérer les critères de recherche de la requête
    type_vehicule = request.args.get('type_vehicule')
    marque = request.args.get('marque')
    couleur = request.args.get('couleur')
    fournisseur = request.args.get('fournisseur')

    # Construire la requête de recherche
    query = Automobile.query

    if type_vehicule:
        query = query.filter(Automobile.type_vehicule == type_vehicule)
    if marque:
        query = query.filter(Automobile.marque.like(f'%{marque}%'))
        
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
            'puissance_maximale': str(automobile.puissance_maximale),
            'vitesse_maximale': str(automobile.vitesse_maximale),
            'moteur': str(automobile.moteur),
            'type_vehicule': automobile.type_vehicule,
            'couleur': automobile.couleur,
            'date_enregistrement': automobile.date_enregistrement.isoformat(),
            'fournisseur_info': {
                'id': automobile.fournisseur.id,
                'nom_fournisseur': automobile.fournisseur.nom_fournisseur,
                'email': automobile.fournisseur.email,
                'numero_telephone': automobile.fournisseur.numero_telephone,
                'logo_fournisseur': automobile.fournisseur.logo_fournisseur,
                'date_enregistrement': automobile.fournisseur.date_enregistrement,
                'localisation': automobile.fournisseur.localisation,
                'adresse': automobile.fournisseur.adresse
            },
            'description': automobile.description,
            'image': automobile.image
        })

    return jsonify(automobiles)


def get_duration(date_enregistrement):
    delta = datetime.now() - date_enregistrement
    duration = f"{delta.days} jours, {delta.seconds // 3600} heures, {(delta.seconds // 60) % 60} minutes"
    return duration
if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0')


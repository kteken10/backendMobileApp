from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime


db = SQLAlchemy()

class Visiteur(db.Model):
    # Modèle pour les visiteurs
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    numero_telephone = db.Column(db.String(255), nullable=False)
    photo_profil = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    date_enregistrement = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Fournisseur(db.Model):
    # Modèle pour les fournisseurs
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_fournisseur = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    numero_telephone = db.Column(db.String(255), nullable=False)
    logo_fournisseur = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    date_enregistrement = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    localisation = db.Column(db.String(255), nullable=False)
    adresse = db.Column(db.String(255), nullable=False)

class Automobile(db.Model):
    # Modèle pour les automobiles
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    marque = db.Column(db.String(255), nullable=False)
    prix = db.Column(db.Numeric, nullable=False)
    puissance_maximale = db.Column(db.Numeric, nullable=False)
    vitesse_maximale = db.Column(db.Numeric, nullable=False)
    moteur = db.Column(db.Numeric, nullable=False)
    type_vehicule = db.Column(db.String(255), nullable=False)
    couleur = db.Column(db.String(255), nullable=False)
    date_enregistrement = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fournisseur_id = db.Column(db.Integer, db.ForeignKey('fournisseur.id'))
    description = db.Column(db.String(10000), nullable=False, default='')
    fournisseur = db.relationship('Fournisseur', backref=db.backref('automobiles', lazy=True))

class ImageAutomobile(db.Model):
    # Modèle pour les images associées aux automobiles
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    automobile_id = db.Column(db.Integer, db.ForeignKey('automobile.id'), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    automobile = db.relationship('Automobile', backref=db.backref('images', lazy=True))


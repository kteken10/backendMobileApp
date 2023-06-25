from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Visiteur(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    numero_telephone = db.Column(db.String(255), nullable=False)
    photo_profil = db.Column(db.String(255))
    date_enregistrement = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Fournisseur(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_fournisseur = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    numero_telephone = db.Column(db.String(255), nullable=False)
    logo_fournisseur = db.Column(db.String(255))
    date_enregistrement = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    localisation = db.Column(db.String(255), nullable=False)
    adresse = db.Column(db.String(255), nullable=False)

class Automobile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    marque = db.Column(db.String(255), nullable=False)
    prix = db.Column(db.Numeric, nullable=False)
    type_vehicule = db.Column(db.String(255), nullable=False)
    couleur = db.Column(db.String(255), nullable=False)
    date_enregistrement = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fournisseur_id = db.Column(db.Integer, db.ForeignKey('fournisseur.id'))
    fournisseur = db.relationship('Fournisseur', backref=db.backref('automobiles', lazy=True))
    image = db.Column(db.String(255), nullable=False)


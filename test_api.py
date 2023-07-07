#Fichier qui utilise pytest pour les test unitaire conernant l'API DE l'APP
import pytest 
import os
from os import environ as env
from flask_testing import TestCase
from app import app

from dotenv import find_dotenv, load_dotenv
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
    
    
class TestApi(TestCase):
    def create_app(self):
        return app
     
    def test_create_visiteur(self):
        data = {
            'nom': 'John Doe',
            'email': 'johnatnhat barbier@example.com',
            'numero_telephone': '123456789',
            'password': 'password123'
        }
        response = self.client.post('/visiteurs', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Visiteur created successfully')    
    def test_get_visiteur(self):
        visiteur_id = 1

        response = self.client.get(f'/visiteurs/{visiteur_id}')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], 'Token missing')

        # Utiliser un token valide pour accéder à un visiteur spécifique
        token = env.get("TOKEN_TEST", None)
        headers = {'Authorization': token}
        response = self.client.get(f'/visiteurs/{visiteur_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)

    def test_delete_all_visiteurs(self):
        response = self.client.delete('/visiteurs')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Tous les visiteurs ont été supprimés avec succès')    
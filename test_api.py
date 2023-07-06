#Fichier qui utilise pytest pour les test unitaire conernant l'API DE l'APP
import pytest 
from flask_testing import TestCase
from app import app

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